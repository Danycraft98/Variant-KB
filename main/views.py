from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.core import mail
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.forms.models import model_to_dict
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import redirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse

import datetime
import pandas
import urllib
from weasyprint import HTML
from api.models import *
from .tables import GeneTable, VariantTable, UploadTable, DiseaseTable, HistoryTable, add_evidence


@login_required
def index(request):
    gene_list = GeneTable(Gene.objects.all())
    return render(request, 'variants/index.html', {'table': gene_list, 'title': 'List of Genes'})


@login_required
def search(request):
    if request.POST:
        search_query = request.POST.dict()
        name = request.POST.get("name")
        if name:
            try:
                item = Gene.objects.get(name=name)
                return redirect('gene', gene_id=item.id)
            except Gene.DoesNotExist:
                pass
        else:
            search_query = {key: value for key, value in search_query.items() if value != ''}
            search_query.pop("csrfmiddlewaretoken")
            return redirect('/variants?' + urllib.parse.urlencode(search_query))
        return render(request, 'general/search.html', {'title': 'List of Genes'})
    return render(request, 'general/search.html', {'title': 'List of Genes'})


@login_required
def account_request(request):
    if request.POST:
        send_mail(
            'Account User Level Request',
            'Dear Sir/Madam,\nI am requesting for user level ' + request.POST.get("level", "") + ". My username is " + request.user.username + "\nRegards,\n" + request.POST.get("name", "anonymous"),
            request.POST.get("email", "anonymous@variant.com"),
            ['lee.daniel.jhl@gmail.com'],
            fail_silently=False
        )
        return render(request, 'general/request.html', {'title': 'List of Genes'})
    return render(request, 'general/request.html', {'title': 'List of Genes'})


@login_required
def variants(request):
    if request.GET:
        variant_list = VariantTable(Variant.objects.filter(chromosome__contains=request.GET.get("chromosome",""), p__contains=request.GET.get("p",""), c__contains=request.GET.get("c",""), ref__contains=request.GET.get("ref", ""), alt__contains=request.GET.get("alt", "")))
    else:
        variant_list = VariantTable(Variant.objects.all())
    return render(request, 'variants/index.html', {'table': variant_list, 'title': 'List of Variants'})


@login_required
def gene(request, gene_name):
    try:
        item = Gene.objects.get(name=gene_name)
    except Gene.DoesNotExist:
        raise Http404("Gene does not exist")
    variant_list = VariantTable(item.variants.all())
    return render(request, 'variants/index.html', {'item': item, 'table': variant_list, 'title': 'List of Variants'})


@login_required
def variant(request, gene_name, variant_p):
    if not request.user.is_staff:
        messages.warning(request, 'You are not authorized to edit variants.')
        return HttpResponseRedirect(reverse('gene', args=[gene_name]))
    try:
        item = Variant.objects.get(gene__name=gene_name, protein=variant_p)
        score_items = PathItem.objects.all()
    except Variant.DoesNotExist:
        raise Http404("Variant does not exist")
    if item.branch == 'gp':
        return render(request, 'variants/gp_form.html', {'item': item, 'items': score_items})
    else:
        return render(request, 'variants/so_form.html', {'item': item})


@login_required
def upload(request):
    if "add_or_update" in request.POST:
        variant_ids = request.POST.get("variant_ids").split(",")
        for variant_id in variant_ids:
            if variant_id in request.POST.getlist("add_or_update"):
                variant_item = Variant.objects.get(pk=variant_id)
                if variant_item.existing:
                    existing = variant_item.existing
                    data = model_to_dict(variant_item)
                    data.pop('id', None)
                    data.pop('existing', None)
                    existing.update(**data)
                    variant_item.delete()
            else:
                Variant.objects.get(pk=int(variant_id)).delete()
        return HttpResponseRedirect(reverse('index'))
    exists_dict = {"yes": [], "no": []}
    raw_data = pandas.read_excel(request.FILES.get("file"), dtype=str)
    raw_data.fillna('na', inplace=True)

    variant_ids = []
    raw_data.rename(columns={'ExonicFunc.UHNCLGGene':'exonic_function'}, inplace=True)
    raw_data.columns = raw_data.columns.str.lower()
    for _, row in raw_data.iterrows():
        if "chr" not in row[0]:
            continue
        gene_name = row.pop('gene')
        exist_variants = Variant.objects.filter(gene__name=gene_name, protein=row.get("protein"))
        count = exist_variants.count()
        raw_hotspots = str(row.pop('cancerhotspots')).split("|")

        try:
            gene_item = Gene.objects.get(name=gene_name)
        except Gene.DoesNotExist:
            gene_item = Gene.objects.create(name=gene_name, pub_date=datetime.datetime.now())

        variant = Variant.objects.create(branch=request.POST.get("data_type"), gene=gene_item, **row)
        if "consequence" in row or count == 0:
            History.objects.create(content="Upload", user=request.user, timestamp=datetime.datetime.now(), variant=variant)
            exists_dict["no"].append(variant)
        else:
            variant.existing = exist_variants.first()
            exists_dict["yes"].append(variant)
        variant_ids.append(str(variant.id))
        for hotspot in raw_hotspots:
            if hotspot == "na":
                break
            values = hotspot.split(":")
            cancer = CancerHotspot.objects.create(hotspot=values[0], variant=variant)
            if len(values) > 1:
                cancer.count = int(values[1])
                cancer.save()

    return render(request, 'general/uploaded.html', {'exist': UploadTable(exists_dict["yes"]), 'new': UploadTable(exists_dict["no"]), "variant_ids": ",".join(variant_ids), 'title': 'Uploads'})


@login_required
def save(request, gene_name, variant_p):
    try:
        review_val = request.POST.getlist('review', ["n"])[-1]
        filter = Variant.objects.filter(gene__name=gene_name, protein=variant_p)
        if review_val == "r":
            filter.update(reviewed_date=datetime.datetime.now(), review_user=request.user)
        elif review_val == "a":
            filter.update(approved_date=datetime.datetime.now(), approve_user=request.user)
        filter.update(content=request.POST.get("variant_report", ""), germline_content=request.POST.get("variant_germline_report", ""), reviewed=review_val)

        Gene.objects.filter(name=gene_name).update(content=request.POST.get("gene_report", ""), germline_content=request.POST.get("gene_germline_report", ""))
        item = Variant.objects.get(gene__name=gene_name, protein=variant_p)

        i = 1
        while request.POST.get("d" + str(i) + "_disease"):
            if not request.POST.get("d" + str(i) + "_id").isdigit():
                dx_id = Disease.objects.create(name=request.POST.get("d" + str(i) + "_disease"), report=request.POST.get("d" + str(i) + "_desc"), others=request.POST.get("d" + str(i) + "_others"), variant=item)
            else:
                Disease.objects.filter(pk=request.POST.get("d" + str(i) + "_id")).update(name=request.POST.get("d" + str(i) + "_disease"), report=request.POST.get("d" + str(i) + "_desc"), others=request.POST.get("d" + str(i) + "_others"))
                dx_id = Disease.objects.get(pk=request.POST.get("d" + str(i) + "_id"))

            if item.branch == 'gp':
                for element in ITEMS.keys():
                    item_id = PathItem.objects.get(key=element)
                    add_evidence(request, "d" + str(i) + "_" + element, dx_id, item, item_id)
                for_score = request.POST.get("d" + str(i) + "_for_score")
                against_score = request.POST.get("d" + str(i) + "_against_score")
                if Score.objects.filter(disease=dx_id):
                    Score.objects.filter(disease=dx_id).update(for_score=for_score, against_score=against_score)
                else:
                    Score.objects.get_or_create(for_score=for_score, against_score=against_score, disease=dx_id)
            else:
                j = 1
                func_sig = request.POST.get("d" + str(i) + "_func_sig")
                while request.POST.get("d" + str(i) + "_fc" + str(j)):
                    if not request.POST.get("d" + str(i) + "_fc" + str(j) + "_id").isdigit():
                        func_id = Functional.objects.create(key=func_sig, value=request.POST.get("d" + str(i) + "_fc" + str(j)), disease=dx_id)
                    else:
                        func_id = Functional.objects.get(pk=request.POST.get("d" + str(i) + "_fc" + str(j) + "_id"))
                        Functional.objects.filter(pk=request.POST.get("d" + str(i) + "_fc" + str(j) + "_id")).update(key=func_sig, value=request.POST.get("d" + str(i) + "_fc" + str(j)))

                    add_evidence(request, "d" + str(i) + "_fc" + str(j) + "_etype1", dx_id, item, func_id)
                    j += 1
                add_evidence(request, "d" + str(i) + "_etype2", dx_id, item)
            for report_id, report, field_name in zip(request.POST.getlist("d" + str(i) + "_report_id"), request.POST.getlist("d" + str(i) + "_report"), request.POST.getlist("d" + str(i) + "_report_name")):
                print(report)
                if len(report) > 0:
                    if not report_id.isdigit():
                        Report.objects.create(name=field_name, content=report, gene=item.gene, variant=item, disease=dx_id)
                    else:
                        Report.objects.filter(pk=report_id).update(name=field_name, content=report)
            i += 1
    except Variant.DoesNotExist:
        raise Http404("Variant does not exist")
    return HttpResponseRedirect(reverse('variant_text', args=(gene_name,variant_p)))


@login_required
def variant_text(request, gene_name, variant_p):
    try:
        item = Variant.objects.get(protein=variant_p, gene__name=gene_name)
    except Variant.DoesNotExist:
        raise Http404("Variant does not exist")
    return render(request, 'variants/' + item.branch + '_detail.html', {'item': item})


@login_required
def export(request, gene_name, variant_p):
    try:
        item = Variant.objects.get(gene__name=gene_name, protein=variant_p)
        disease_list = DiseaseTable(item.diseases.all())
    except Variant.DoesNotExist:
        raise Http404("Variant does not exist")
    return render(request, 'variants/index.html', {'title': 'Export for Variant', 'item': item, 'table': disease_list})


def exported(request, gene_name, variant_p):
    try:
        item = Variant.objects.get(gene__name=gene_name, protein=variant_p)
    except Variant.DoesNotExist:
        raise Http404("Variant does not exist")
    diseases = Disease.objects.filter(name__in=request.POST.getlist("disease"))
    if item.branch == 'gp':
        html_string = render_to_string('general/gp_export.html', {'item': item, 'diseases': diseases})
    else:
        html_string = render_to_string('general/so_export.html', {'item': item, 'diseases': diseases})

    html = HTML(string=html_string)
    html.write_pdf(target='/tmp/report.pdf')

    fs = FileSystemStorage('/tmp')
    with fs.open('report.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="report.pdf"'
        return response


def history(request, gene_name, variant_p):
    try:
        item = Variant.objects.get(gene__name=gene_name, protein=variant_p)
        histories = HistoryTable([h for h in item.history.all()])
    except Variant.DoesNotExist:
        raise Http404("Variant does not exist")
    return render(request, 'variants/index.html', {'item': item, 'table': histories, 'title': 'History'})
