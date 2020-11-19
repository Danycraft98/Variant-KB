from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import redirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse

import datetime
import json
import pandas
import urllib
from weasyprint import HTML, CSS
from api.models import *
from .tables import GeneTable, VariantTable, DiseaseTable, HistoryTable, add_evidence


@login_required
def index(request):
    gene_list = GeneTable(Gene.objects.all())
    return render(request, 'variants/index.html', {'table': gene_list, 'title': 'List of Genes'})


@login_required
def search(request):
    if request.POST:
        search_query = request.POST.dict()
        name = request.POST.get('name')
        if name:
            try:
                item = Gene.objects.get(name=name)
                return redirect('gene', gene_id=item.id)
            except Gene.DoesNotExist:
                pass
        else:
            search_query = {key: value for key, value in search_query.items() if value != ''}
            search_query.pop('csrfmiddlewaretoken')
            return redirect('/variants?' + urllib.parse.urlencode(search_query))
        return render(request, 'general/search.html', {'title': 'List of Genes'})
    return render(request, 'general/search.html', {'title': 'List of Genes'})


@login_required
def account_request(request):
    if request.POST:
        send_mail(
            'Account User Level Request',
            'Dear Sir/Madam,\nI am requesting for user level ' + request.POST.get('level', '') + '. My username is ' + request.user.username + '\nRegards,\n' + request.POST.get('name', 'anonymous'),
            request.POST.get('email', 'anonymous@variant.com'),
            ['lee.daniel.jhl@gmail.com'],
            fail_silently=False
        )
        return render(request, 'general/request.html', {'title': 'List of Genes'})
    return render(request, 'general/request.html', {'title': 'List of Genes'})


@login_required
def variants(request):
    if request.GET:
        variant_list = VariantTable(Variant.objects.filter(chr__contains=request.GET.get('chromosome', ''), protein__contains=request.GET.get('protein', ''), cdna__contains=request.GET.get('cdna',''), ref__contains=request.GET.get('ref', ''), alt__contains=request.GET.get('alt', '')))
    else:
        variant_list = VariantTable(Variant.objects.all())
    return render(request, 'variants/index.html', {'table': variant_list, 'title': 'List of Variants'})


@login_required
def gene(request, gene_name):
    try:
        item = Gene.objects.get(name=gene_name)
    except Gene.DoesNotExist:
        raise Http404('Gene does not exist')
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
        raise Http404('Variant does not exist')
    return render(request, 'variants/form.html', {'item': item, 'items': score_items})


@login_required
def upload(request):
    exists_dict = {'yes': [], 'no': []}
    if 'dict' not in request.POST:
        raw_data = pandas.read_excel(request.FILES.get('file'), dtype=str, header=20)
        raw_data.fillna('na', inplace=True)
        default_header = list(raw_data.columns)
        [default_header.remove(key) for key in ['IGV', 'UCSC Genome Browser', 'HGMD']]
        raw_data = raw_data.rename(columns=str.lower)
    else:
        raw_data = pandas.DataFrame.from_records(json.loads(request.POST.get('dict')))
        default_header = list(raw_data.columns)
        [default_header.remove(key) for key in ['igv', 'ucsc genome browser', 'hgmd']]
        raw_data.rename(columns={'exonicfunc.uhnclggene': 'exonic_function'}, inplace=True)

    for _, row in raw_data.iterrows():
        if 'chr' not in row:
            continue

        gene_name = row.get('gene')
        [row.pop(key) for key in ['igv', 'ucsc genome browser', 'hgmd']]
        exist_variants = Variant.objects.filter(gene__name=gene_name, protein=row.get('protein'))
        count = exist_variants.count()
        if 'add_or_update' in request.POST and row.get('protein') in request.POST.getlist('add_or_update'):
            row['tcga'] = row.pop('tcga#occurances')
            raw_cancerhotspot = str(row.pop('cancerhotspots')).split('|')
            row.pop('gene')

            try:
                gene_item = Gene.objects.get(name=gene_name)
            except Gene.DoesNotExist:
                gene_item = Gene.objects.create(name=gene_name, pub_date=datetime.datetime.now())

            if 'consequence' in row or count == 0:
                variant1 = Variant.objects.create(gene=gene_item, **row)
                History.objects.create(content='Upload', user=request.user, timestamp=datetime.datetime.now(), variant=variant1)
            else:
                exist_variants.update(**row)
                variant1 = exist_variants.first()
                History.objects.create(content='Updated', user=request.user, timestamp=datetime.datetime.now(), variant=variant1)

            for hotspot in raw_cancerhotspot:
                if hotspot == 'na':
                    break
                values = hotspot.split(':')
                cancer = CancerHotspot.objects.create(hotspot=values[0], variant=variant1)
                if len(values) > 1:
                    cancer.count = int(values[1])
                    cancer.save()
        else:
            if 'consequence' in row or count == 0:
                exists_dict['no'].append(row)
            else:
                exists_dict['yes'].append(row)
    if 'dict' in request.POST:
        return HttpResponseRedirect(reverse('index'))
    else:
        new = pandas.DataFrame.from_records(exists_dict['no'])
        exist = pandas.DataFrame.from_records(exists_dict['yes'])
        if not new.empty:
            new.columns = default_header
            new = new[['Chr', 'cDNA', 'Protein', 'Transcript', 'Start', 'End', 'Ref', 'Alt', default_header[5]] + default_header[9:]].rename(columns={"Chr": "Chromosome", "cDNA": "C.", 'Protein': 'P.'})
        if not exist.empty:
            exist.columns = default_header
            exist = exist[['Chr', 'cDNA', 'Protein', 'Transcript', 'Start', 'End', 'Ref', 'Alt', default_header[5]] + default_header[9:]].rename(columns={"Chr": "Chromosome", "cDNA": "C.", 'Protein': 'P.'})

        exist_html = exist.to_html(classes='exist table table-bordered table-hover', justify='left')
        new_html = new.to_html(classes='exist table table-bordered table-hover', justify='left')
        return render(request, 'general/uploaded.html', {'tables': (new_html, exist_html), 'is_empty': (new.empty, exist.empty), 'dict': raw_data.to_json(), 'title': 'Uploads'})


@login_required
def save(request, gene_name, variant_p):
    try:
        review_val = request.POST.getlist('review', ['n'])[-1]
        filter_val = Variant.objects.filter(gene__name=gene_name, protein=variant_p)
        if review_val == 'r':
            filter_val.update(reviewed_date=datetime.datetime.now(), review_user=request.user)
        elif review_val == 'a':
            filter_val.update(approved_date=datetime.datetime.now(), approve_user=request.user)
        filter_val.update(content=request.POST.get('variant_report', ''), germline_content=request.POST.get('variant_germline_report', ''), reviewed=review_val)

        Gene.objects.filter(name=gene_name).update(content=request.POST.get('gene_report', ''), germline_content=request.POST.get('gene_germline_report', ''))
        item = Variant.objects.get(gene__name=gene_name, protein=variant_p)

        i = 2
        while request.POST.get('d' + str(i) + '_disease'):
            if not request.POST.get('d' + str(i) + '_id').isdigit():
                dx_id = Disease.objects.create(name=request.POST.get('d' + str(i) + '_disease'), report=request.POST.get('d' + str(i) + '_desc'), others=request.POST.get('d' + str(i) + '_others'), variant=item)
            else:
                Disease.objects.filter(pk=request.POST.get('d' + str(i) + '_id')).update(name=request.POST.get('d' + str(i) + '_disease'), report=request.POST.get('d' + str(i) + '_desc'), others=request.POST.get('d' + str(i) + '_others'))
                dx_id = Disease.objects.get(pk=request.POST.get('d' + str(i) + '_id'))

            if request.POST.get('d' + str(i) + '_type') == 'gp':
                for element in ITEMS.keys():
                    item_id = PathItem.objects.get(key=element)
                    add_evidence(request, 'd' + str(i) + '_' + element, dx_id, item, item_id)
                for_score = request.POST.get('d' + str(i) + '_for_score')
                against_score = request.POST.get('d' + str(i) + '_against_score')
                if Score.objects.filter(disease=dx_id):
                    Score.objects.filter(disease=dx_id).update(for_score=for_score, against_score=against_score)
                else:
                    Score.objects.get_or_create(for_score=for_score, against_score=against_score, disease=dx_id)
            else:
                j = 1
                func_sig = request.POST.get('d' + str(i) + '_func_sig')
                while request.POST.get('d' + str(i) + '_fc' + str(j)):
                    if not request.POST.get('d' + str(i) + '_fc' + str(j) + '_id').isdigit():
                        func_id = Functional.objects.create(key=func_sig, value=request.POST.get('d' + str(i) + '_fc' + str(j)), disease=dx_id)
                    else:
                        func_id = Functional.objects.get(pk=request.POST.get('d' + str(i) + '_fc' + str(j) + '_id'))
                        Functional.objects.filter(pk=request.POST.get('d' + str(i) + '_fc' + str(j) + '_id')).update(key=func_sig, value=request.POST.get('d' + str(i) + '_fc' + str(j)))

                    add_evidence(request, 'd' + str(i) + '_fc' + str(j) + '_etype1', dx_id, item, func_id)
                    j += 1
                add_evidence(request, 'd' + str(i) + '_etype2', dx_id, item)
            for report_id, report, field_name in zip(request.POST.getlist('d' + str(i) + '_report_id'), request.POST.getlist('d' + str(i) + '_report'), request.POST.getlist('d' + str(i) + '_report_name')):
                if len(report) > 0:
                    if not report_id.isdigit():
                        Report.objects.create(name=field_name, content=report, gene=item.gene, variant=item, disease=dx_id)
                    else:
                        Report.objects.filter(pk=report_id).update(name=field_name, content=report)
            i += 1
    except Variant.DoesNotExist:
        raise Http404('Variant does not exist')
    return HttpResponseRedirect(reverse('variant_text', args=(gene_name, variant_p)))


@login_required
def variant_text(request, gene_name, variant_p):
    try:
        item = Variant.objects.get(protein=variant_p, gene__name=gene_name)
    except Variant.DoesNotExist:
        raise Http404('Variant does not exist')
    return render(request, 'variants/detail.html', {'item': item})


@login_required
def export(request, gene_name, variant_p):
    try:
        item = Variant.objects.get(gene__name=gene_name, protein=variant_p)
        disease_list = DiseaseTable(item.diseases.all())
    except Variant.DoesNotExist:
        raise Http404('Variant does not exist')
    return render(request, 'variants/index.html', {'title': 'Export for Variant', 'item': item, 'table': disease_list})


def exported(request, gene_name, variant_p):
    try:
        item = Variant.objects.get(gene__name=gene_name, protein=variant_p)
    except Variant.DoesNotExist:
        raise Http404('Variant does not exist')
    diseases = Disease.objects.filter(name__in=request.POST.getlist('disease'))
    html = HTML(string=render_to_string('general/export.html', {'item': item, 'diseases': diseases}))
    html.write_pdf(target='/tmp/report.pdf', stylesheets=[CSS('static/bootstrap.min.css')])

    fs = FileSystemStorage('/tmp')
    with fs.open('report.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = "attachment; filename='report.pdf'"
        return response


def history(request, gene_name, variant_p):
    try:
        item = Variant.objects.get(gene__name=gene_name, protein=variant_p)
        histories = HistoryTable([h for h in item.history.all()])
    except Variant.DoesNotExist:
        raise Http404('Variant does not exist')
    return render(request, 'variants/index.html', {'item': item, 'table': histories, 'title': 'History'})
