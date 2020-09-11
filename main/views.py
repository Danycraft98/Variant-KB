from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.urls import reverse

import datetime
import pandas
import urllib
from weasyprint import HTML
from api.models import *
from .tables import GeneTable, VariantTable, DiseaseTable, HistoryTable, add_evidence


# Create your views here.
@login_required
def index(request):
	gene_list = GeneTable(Gene.objects.all())
	return render(request, 'variants/index.html', {'table': gene_list, 'title': 'List of Genes'})


# Create your views here.
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


# Create your views here.
@login_required
def variants(request):
	if request.GET:
		variant_list = VariantTable(Variant.objects.filter(**request.GET.dict()))
	else:
		variant_list = VariantTable(Variant.objects.all())
	return render(request, 'variants/index.html', {'table': variant_list, 'title': 'List of Variants'})


@login_required
def gene(request, gene_id):
	try:
		item = Gene.objects.get(pk=gene_id)
	except Gene.DoesNotExist:
		raise Http404("Gene does not exist")
	variant_list = VariantTable(item.variants.all())
	return render(request, 'variants/index.html', {'item': item, 'table': variant_list, 'title': 'List of Variants'})


@login_required
def variant(request, variant_id):
	try:
		item = Variant.objects.get(pk=variant_id)
		score_items = PathItem.objects.all()
	except Variant.DoesNotExist:
		raise Http404("Variant does not exist")
	if item.branch == 'gp':
		return render(request, 'variants/gp_form.html', {'item': item, 'items': score_items})
	else:
		return render(request, 'variants/so_form.html', {'item': item})


@login_required
def upload(request):
	spreadsheet = request.FILES.get("file")
	if spreadsheet.name.split('.')[-1] == "csv":
		raw_data = pandas.read_csv(request.FILES.get("file"))
	else:
		raw_data = pandas.read_excel(request.FILES.get("file"))
	for _, row in raw_data.iterrows():
		exist_variants = Variant.objects.filter(gene__name=row.get("gene")).filter(Q(c=row.get("c")) | Q(p=row.get("p")))
		gene_name = row.pop('gene')
		try:
			gene_item = Gene.objects.get(name=gene_name)
		except Gene.DoesNotExist:
			gene_item = Gene.objects.create(name=gene_name, pub_date=datetime.datetime.now())
		if "consequence" in row or exist_variants.count() == 0:
			Variant.objects.create(branch=request.POST.get("data_type"), gene=gene_item, **row)
		else:
			print(exist_variants.count())
	return HttpResponseRedirect(reverse('index'))


@login_required
def save(request, variant_id):
	try:
		item = Variant.objects.get(pk=variant_id)

		i = 1
		while request.POST.get("d" + str(i) + "_disease"):
			if not request.POST.get("d" + str(i) + "_id").isdigit():
				main_item = Disease.objects.create(name=request.POST.get("d" + str(i) + "_disease"), report=request.POST.get("d" + str(i) + "_desc"), others=request.POST.get("d" + str(i) + "_others"), variant=item)
				dx_id = Disease.objects.get(pk=main_item.pk)
			else:
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
						main_item = Functional.objects.create(key=func_sig, value=request.POST.get("d" + str(i) + "_fc" + str(j)), disease=dx_id)
						func_id = Functional.objects.get(pk=main_item.pk)
					else:
						func_id = Functional.objects.get(pk=request.POST.get("d" + str(i) + "_fc" + str(j) + "_id").isdigit())

					add_evidence(request, "d" + str(i) + "_fc" + str(j) + "_etype1", dx_id, item, func_id)
					j += 1
				add_evidence(request, "d" + str(i) + "_etype2", dx_id, item)
			for report_id, report, field_name in zip(request.POST.getlist("d" + str(i) + "_report_id"), request.POST.getlist("d" + str(i) + "_report"), request.POST.getlist("d" + str(i) + "_report_name")):
				if not report_id.isdigit() and len(report) > 0:
					Report.objects.create(name=field_name, content=report, disease=dx_id)
			i += 1
	except Variant.DoesNotExist:
		raise Http404("Variant does not exist")
	return HttpResponseRedirect(reverse('variant_text', args=(variant_id,)))


@login_required
def variant_text(request, variant_id):
	try:
		item = Variant.objects.get(pk=variant_id)
	except Variant.DoesNotExist:
		raise Http404("Variant does not exist")
	return render(request, 'variants/' + item.branch + '_detail.html', {'item': item})


@login_required
def export(request, variant_id):
	try:
		item = Variant.objects.get(pk=variant_id)
		disease_list = DiseaseTable(item.diseases.all())
	except Variant.DoesNotExist:
		raise Http404("Variant does not exist")
	return render(request, 'variants/index.html', {'title': 'Export for Variant ' + item.name, 'item': item, 'table': disease_list})


def exported(request, variant_id):
	try:
		item = Variant.objects.get(pk=variant_id)
	except Variant.DoesNotExist:
		raise Http404("Variant does not exist")
	diseases = Disease.objects.filter(name__in=request.POST.getlist("disease"))
	if item.branch == 'gp':
		html_string = render_to_string('general/gp_export.html', {'item': item, 'diseases': diseases})
	else:
		html_string = render_to_string('general/so_export.html', {'item': item, 'diseases': diseases})

	html = HTML(string=html_string)
	html.write_pdf(target='/tmp/report_' + item.name + '.pdf')

	fs = FileSystemStorage('/tmp')
	with fs.open('report_' + item.name + '.pdf') as pdf:
		response = HttpResponse(pdf, content_type='application/pdf')
		response['Content-Disposition'] = 'attachment; filename="report_' + item.name + '.pdf"'
		return response


def history(request, variant_id):
	try:
		item = Variant.objects.get(pk=variant_id)
		print(item.history.all())
		histories = HistoryTable([h for h in item.history.all()])
	except Variant.DoesNotExist:
		raise Http404("Variant does not exist")
	return render(request, 'variants/index.html', {'item': item, 'table': histories, 'title': 'History of ' + str(item)})
