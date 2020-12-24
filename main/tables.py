from django_tables2.utils import A
import django_tables2 as tables
import datetime

from api.models import Gene, Variant, Disease, Evidence, SubEvidence, History


def add_evidence(request, prefix, dx_id, variant, item=None):
    for i, (e_id, source_type, source_id, statement) in enumerate(zip(request.POST.getlist(prefix + "_id"), request.POST.getlist(prefix + "_st"), request.POST.getlist(prefix + "_s"), request.POST.getlist(prefix + "_e"))):
        if e_id.isdigit():
            evidence = Evidence.objects.get(pk=e_id)
            Evidence.objects.filter(pk=e_id).update(source_type=source_type, source_id=source_id, statement=statement)
        else:
            sub_item = Evidence.objects.create(disease=dx_id, source_type=source_type, source_id=source_id, statement=statement)
            if item.__class__.__name__ == "PathItem":
                Evidence.objects.filter(pk=sub_item.pk).update(item=item)
            elif item.__class__.__name__ == "Functional":
                Evidence.objects.filter(pk=sub_item.pk).update(functional=item)
            evidence = Evidence.objects.get(pk=sub_item.pk)

        if request.POST.getlist(prefix + "_sig"):
            if evidence.subevidences.count() > 0:
                evidence.subevidences.update(level=request.POST.getlist(prefix + "_level")[i], evid_sig=request.POST.getlist(prefix + "_sig")[i], evid_dir=request.POST.getlist(prefix + "_dir")[i], clin_sig=request.POST.getlist(prefix + "_clin_sig")[i],
                                             drug_class=request.POST.getlist(prefix + "_drug")[i], evid_rating=request.POST.getlist(prefix + "_rating")[i], evidence=evidence)
            else:
                SubEvidence.objects.create(level=request.POST.getlist(prefix + "_level")[i], evid_sig=request.POST.getlist(prefix + "_sig")[i], evid_dir=request.POST.getlist(prefix + "_dir")[i], clin_sig=request.POST.getlist(prefix + "_clin_sig")[i],
                                           drug_class=request.POST.getlist(prefix + "_drug")[i], evid_rating=request.POST.getlist(prefix + "_rating")[i], evidence=evidence)
        History.objects.create(content=statement, object=evidence, user=request.user, timestamp=datetime.datetime.now(), variant=variant)


class GeneTable(tables.Table):
    name = tables.LinkColumn('gene', args=[A('name')], text=lambda record: record.name, empty_values=())
    variants = tables.TemplateColumn('{{ record.variants.count }} variant(s)', verbose_name="Variants")

    class Meta:
        model = Gene
        orderable = False
        sequence = ('name', 'variants')
        exclude = ('id', 'exon', 'pub_date', 'content', 'germline_content')
        attrs = {"class": "dataTable nowrap table table-bordered table-hover"}


class VariantTable(tables.Table):
    edit = tables.LinkColumn('variant', args=[A('gene__name'), A('protein')], text="edit", empty_values=())
    variant_detail = tables.LinkColumn('variant_text', args=[A('gene.name'), A('protein')], text='detail', empty_values=())
    diseases = tables.TemplateColumn('{{ record.diseases.count }} disease(s)', verbose_name='Diseases')
    history = tables.TemplateColumn('{{ record.history.first.timestamp }}', verbose_name='Upload Date')
    recent = tables.TemplateColumn('{{ record.history.last.timestamp }}', verbose_name='Last Modified Date')

    class Meta:
        model = Variant
        orderable = True
        # order_by = ('-history',)
        sequence = ('edit', 'variant_detail', 'gene', 'chr', 'cdna', 'protein', 'transcript')
        exclude = ('id', 'genome_build', 'consequence', 'exonic_function', 'content',
                   'germline_content', 'af', 'af_popmax', 'cosmic70', 'clinvar', 'insilicodamaging',
                   'insilicobenign', 'polyphen2_hdiv_pred', 'polyphen2_hvar_pred', 'sift_pred',
                   'mutationtaster_pred', 'mutationassessor_pred', 'provean_pred', 'lrt_pred', 'tcga',
                   'oncokb', 'oncokb_pmids', 'watson', 'watson_pmids', 'qci', 'qci_pmids', 'jaxckb',
                   'jaxckb_pmids', 'pmkb', 'pmkb_citations', 'civic', 'google', 'alamut')
        attrs = {"class": "dataTable nowrap table table-bordered table-hover"}
        row_attrs = {
            "title": lambda record: '\n'.join([disease.name + ': [' + disease.get_reviewed_display() + ', ' + disease.branch.upper() + ']' for disease in record.diseases.all()])
            if record.diseases.count() > 0 else 'No Disease'
        }

    @staticmethod
    def class_type():
        return "Variant"


class DiseaseTable(tables.Table):
    disease = tables.CheckBoxColumn(checked=True, accessor="name", attrs={'th__input': {'checked': 'checked', 'id': 'selectAll'}})
    functionals = tables.TemplateColumn("{{ record.functionals.count }} functional(s)", verbose_name="Functionals")
    evidences = tables.TemplateColumn("{{ record.evidences.count }} evidence(s)", verbose_name="Evidences")

    class Meta:
        model = Disease
        orderable = False
        sequence = ('disease', 'name', 'functionals', 'evidences')
        exclude = ('id', 'report', 'variant')
        attrs = {
            "class": "nowrap table table-bordered table-hover",
            "style": "display: block; overflow: auto;"
        }

    @staticmethod
    def class_type():
        return "Disease"


class HistoryTable(tables.Table):
    class Meta:
        model = History
        orderable = False
        order_by = "-timestamp"
        sequence = ('timestamp', 'object', 'content', 'user')
        exclude = ('id', 'variant')
        attrs = {"class": "nowrap table table-bordered table-hover"}
