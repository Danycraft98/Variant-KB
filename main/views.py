import json
from urllib import parse

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from weasyprint import HTML, CSS

from .forms import *
from .functions import *
from .tables import *


@login_required
def index(request):
    counts = [Gene.objects.count(), Variant.objects.count(), Disease.objects.count()]
    mini_tables = [GeneCardTable(Gene.objects.all()), VariantCardTable(Variant.objects.all()), DiseaseCardTable(Disease.objects.all())]
    return render(request, 'general/index.html', {'counts': counts, 'mini_tables': mini_tables})


@login_required
def search(request):
    if request.POST:
        search_query = request.POST.dict()
        name = request.POST.get('name')
        if name:
            try:
                item = Gene.objects.get(name=name)
                return redirect('gene', gene_name=item.name)
            except Gene.DoesNotExist:
                pass
        else:
            search_query = {key: value for key, value in search_query.items() if value != ''}
            search_query.pop('csrfmiddlewaretoken')
            return redirect('/variants?' + parse.urlencode(search_query))
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
def genes(request):
    gene_list = GeneTable(Gene.objects.all())
    return render(request, 'variants/index.html', {'table': gene_list, 'title': 'List of Genes'})


@login_required
def variants(request):
    if request.GET:
        variant_list = VariantTable(Variant.objects.filter(chr__contains=request.GET.get('chromosome', ''), protein__contains=request.GET.get('protein', ''), cdna__contains=request.GET.get('cdna', ''), ref__contains=request.GET.get('ref', ''), alt__contains=request.GET.get('alt', '')))
    else:
        variant_list = VariantTable(Variant.objects.all())
    # variant_list.order_by = ('-history',)
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
def variant(request, gene_name, protein):
    if not request.user.is_staff:
        messages.warning(request, 'You are not authorized to edit variants.')
        return HttpResponseRedirect(reverse('gene', args=[gene_name]))

    try:
        item = Variant.objects.get(gene__name=gene_name, protein=protein)
        score_items = PathItem.objects.all()
    except Variant.DoesNotExist:
        raise Http404('Variant does not exist')

    if item.diseases.count() > 0:
        diseases = [item.diseases.filter(branch='so'), item.diseases.filter(branch='gp')]
        forms = [
            SODiseaseFormSet(request.POST or None, request.FILES or None, initial=diseases[0].values()),
            GPDiseaseFormSet(request.POST or None, request.FILES or None, initial=diseases[1].values()),
            EvidenceFormSet(request.POST or None, request.FILES or None),
            PathItemFormSet(request.POST or None, request.FILES or None, initial=PathItem.objects.all().values())
        ]
        for i, form in enumerate(forms[:2]):
            form.extra = len(diseases[i])
    else:
        forms = [
            SODiseaseFormSet(request.POST or None, request.FILES or None),
            GPDiseaseFormSet(request.POST or None, request.FILES or None),
            EvidenceFormSet(request.POST or None, request.FILES or None),
            PathItemFormSet(request.POST or None, request.FILES or None, initial=PathItem.objects.all().values())
        ]

    if request.method == 'POST':
        print(forms[0].errors, forms[1].errors, forms[2].errors, forms[3].errors,)
        for formset in forms[:2]:
            for form in formset:
                if form.is_valid():
                    create_disease(request, item, form.cleaned_data)

        if not forms[0].is_valid() and not forms[1].is_valid():
            return HttpResponseRedirect(reverse('variant', args=(gene_name, protein)))

        return HttpResponseRedirect(reverse('variant_text', args=(gene_name, protein)))

    return render(request, 'variants/form.html', {
        'item': item, 'title': 'Edit - ' + item.protein,
        'items': score_items, 'forms': forms[:2],
        'other_forms': forms[2:]})


@login_required
def upload(request):
    exists_dict = {'yes': [], 'no': []}
    if 'dict' not in request.POST:
        with open(request.FILES.get('file').name, "wb+") as file:
            file.write(request.FILES.get('file').file.getbuffer())
        raw_data = read_file(request.FILES.get('file').name, dtype=str, header=20)
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
        new_html = new.to_html(classes='new table table-bordered table-hover', justify='left')
        return render(request, 'general/uploaded.html', {'tables': (new_html, exist_html), 'is_empty': (new.empty, exist.empty), 'dict': raw_data.to_json(), 'title': 'Uploads'})


@login_required
def variant_text(request, gene_name, protein):
    try:
        item = Variant.objects.get(protein=protein, gene__name=gene_name)
    except Variant.DoesNotExist:
        raise Http404('Variant does not exist')
    return render(request, 'variants/detail.html', {'item': item, 'title': 'Detail - ' + item.protein})


@login_required
def export(request, gene_name, protein):
    try:
        item = Variant.objects.get(gene__name=gene_name, protein=protein)
        disease_list = DiseaseTable(item.diseases.all())
    except Variant.DoesNotExist:
        raise Http404('Variant does not exist')
    return render(request, 'variants/index.html', {'title': 'Export for Variant', 'item': item, 'table': disease_list})


def exported(request, gene_name, protein):
    try:
        item = Variant.objects.get(gene__name=gene_name, protein=protein)
    except Variant.DoesNotExist:
        raise Http404('Variant does not exist')
    diseases = Disease.objects.filter(name__in=request.POST.getlist('disease'))
    html = HTML(string=render_to_string('general/export.html', {'item': item, 'diseases': diseases}))
    html.write_pdf(target='/tmp/report.pdf', stylesheets=[
        CSS('static/css/bootstrap.min.css'), CSS('static/css/main.css')
    ])

    fs = FileSystemStorage('/tmp')
    with fs.open('report.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = "attachment; filename=report.pdf"
        return response


def history(request, gene_name, protein):
    try:
        item = Variant.objects.get(gene__name=gene_name, protein=protein)
        histories = HistoryTable([h for h in item.history.all()])
    except Variant.DoesNotExist:
        raise Http404('Variant does not exist')
    return render(request, 'variants/index.html', {'item': item, 'table': histories, 'title': 'History - ' + item.protein})
