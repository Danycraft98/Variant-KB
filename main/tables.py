from django_tables2.utils import A
import django_tables2 as tables
import datetime

from api.models import Gene, Variant, Disease, Evidence, SubEvidence, History, PathItem


def add_evidence(request, prefix, dx_id, variant, item=None):
	for i, (e_id, source_type, source_id, statement) in enumerate(zip(request.POST.getlist(prefix + "_id"), request.POST.getlist(prefix + "_st"), request.POST.getlist(prefix + "_s"), request.POST.getlist(prefix + "_e"))):
		if e_id.isdigit():
			evidence = Evidence.objects.get(pk=e_id)
			if evidence.statement == statement:
				continue
			Evidence.objects.filter(pk=e_id).update(statement=statement)
		else:
			sub_item = Evidence.objects.create(disease=dx_id, source_type=source_type, source_id=source_id, statement=statement)
			if item.__class__.__name__ == "PathItem":
				Evidence.objects.filter(pk=sub_item.pk).update(item=item)
			elif item.__class__.__name__ == "Functional":
				Evidence.objects.filter(pk=sub_item.pk).update(functional=item)
			evidence = Evidence.objects.get(pk=sub_item.pk)

		if request.POST.getlist(prefix + "_sig"):
			SubEvidence.objects.create(level=request.POST.getlist(prefix + "_level")[i], evid_sig=request.POST.getlist(prefix + "_sig")[i], evid_dir=request.POST.getlist(prefix + "_dir")[i], clin_sig=request.POST.getlist(prefix + "_clin_sig")[i], drug_class=request.POST.getlist(prefix + "_drug")[i], evid_rating=request.POST.getlist(prefix + "_rating")[i], evidence=evidence)
		History.objects.create(content=statement, object=evidence, user=request.user, timestamp=datetime.datetime.now(), variant=variant)


class GeneTable(tables.Table):
	name = tables.LinkColumn('gene', args=[A('id')], text=lambda record: record.name, empty_values=())
	variants = tables.TemplateColumn("{{ record.variants.count }} variant(s)", verbose_name="Variants")

	class Meta:
		model = Gene
		sequence = ('name', 'variants')
		exclude = ('id', 'exon', 'pub_date', 'content')
		attrs = {"class": "dataTable nowrap table table-bordered table-hover"}


class VariantTable(tables.Table):
	edit = tables.LinkColumn('variant', args=[A('id')], text="edit", empty_values=())
	name = tables.LinkColumn('variant_text', args=[A('id')], text=lambda record: record.name, empty_values=())

	class Meta:
		model = Variant
		sequence = ('edit', 'name', 'type', 'exon')
		exclude = ('id', 'gene', 'interpretation', 'c_dna', 'g_dna')
		attrs = {"class": "dataTable nowrap table table-bordered table-hover"}


class CheckBoxColumn2(tables.CheckBoxColumn):
	@property
	def header(self):
		return self.verbose_name


class DiseaseTable(tables.Table):
	disease = CheckBoxColumn2(verbose_name="Disease", accessor="name")
	functionals = tables.TemplateColumn("{{ record.functionals.count }} functional(s)", verbose_name="Functionals")
	evidences = tables.TemplateColumn("{{ record.evidences.count }} evidence(s)", verbose_name="Evidences")

	class Meta:
		model = Disease
		sequence = ('disease', 'name', 'functionals', 'evidences')
		exclude = ('id', 'report', 'variant')
		attrs = {"class": "nowrap table table-bordered table-hover"}


class HistoryTable(tables.Table):
	class Meta:
		model = History
		order_by = "-timestamp"
		sequence = ('timestamp', 'object', 'content', 'user')
		exclude = ('id', 'variant')
		attrs = {"class": "nowrap table table-bordered table-hover"}
