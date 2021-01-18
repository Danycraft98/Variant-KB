from django.db import models

from accounts.models import User
from .constants import *

__all__ = [
    'Gene', 'Variant', 'Disease', 'History', 'CancerHotspot', 'PathItem', 'DxToScore',
    'Score', 'Functional', 'Evidence', 'SubEvidence', 'Report'
]


# Create your models here.
class Gene(models.Model):
    name = models.CharField(max_length=20)
    pub_date = models.DateTimeField('date published')
    content = models.TextField(blank=True)
    germline_content = models.TextField(blank=True)

    def __str__(self):
        return self.name

    @staticmethod
    def class_type():
        return 'Gene'


class Variant(models.Model):
    genome_build = models.CharField(verbose_name='genome build', max_length=10, null=True)
    chr = models.CharField(verbose_name='Chromosome', max_length=6, null=True)
    start = models.CharField(max_length=10, null=True)
    end = models.CharField(max_length=10, null=True)
    ref = models.CharField(max_length=100, null=True)
    alt = models.CharField(max_length=100, null=True)
    transcript = models.CharField(max_length=20)
    cdna = models.CharField(verbose_name='c.', max_length=10, null=True)
    protein = models.CharField(verbose_name='p.', max_length=20)
    consequence = models.CharField(max_length=10, null=True)
    exonic_function = models.CharField(max_length=20, null=True)
    content = models.TextField(blank=True)
    germline_content = models.TextField(blank=True)

    af = models.CharField(verbose_name='AF', max_length=20, null=True)
    af_popmax = models.CharField(verbose_name='AF_popmax', max_length=20, null=True)
    cosmic70 = models.CharField(max_length=20, null=True)
    clinvar = models.CharField(verbose_name='CLINVAR', max_length=20, null=True)
    insilicodamaging = models.CharField(verbose_name='InSilicoDamaging', max_length=20, null=True)
    insilicobenign = models.CharField(verbose_name='InSilicoBenign', max_length=100, null=True)
    polyphen2_hdiv_pred = models.CharField(choices=(
        ('D', 'probably damaging'),
        ('P', 'possibly damaging'),
        ('B', 'benign'),
        ('na', 'na'),
    ), max_length=2, default='na', verbose_name='Polyphen2_HDIV_pred')
    polyphen2_hvar_pred = models.CharField(choices=(
        ('D', 'probably damaging'),
        ('P', 'possibly damaging'),
        ('B', 'benign'),
        ('na', 'na'),
    ), max_length=2, default='na', verbose_name='Polyphen2_HVAR_pred')
    sift_pred = models.CharField(choices=(
        ('D', 'deleterious'),
        ('T', 'tolerated'),
        ('na', 'na'),
    ), max_length=2, default='na', verbose_name='SIFT_pred')
    mutationtaster_pred = models.CharField(choices=(
        ('D', 'deleterious'),
        ('T', 'tolerated'),
        ('na', 'na'),
    ), max_length=2, default='na', verbose_name='MutationTaster_pred')
    mutationassessor_pred = models.CharField(choices=(
        ('H', 'high'),
        ('M', 'medium'),
        ('L', 'low'),
        ('N', 'neutral'),
        ('na', 'na'),
    ), max_length=2, default='na', verbose_name='MutationAssessor_pred')
    provean_pred = models.CharField(choices=(
        ('D', 'deleterious'),
        ('N', 'neutral'),
        ('na', 'na'),
    ), max_length=2, default='na', verbose_name='PROVEAN_pred')
    lrt_pred = models.CharField(choices=(
        ('D', 'deleterious'),
        ('N', 'neutral'),
        ('U', 'unknown'),
        ('na', 'na'),
    ), max_length=2, default='na', verbose_name='PROVEAN_pred')
    tcga = models.CharField(verbose_name='TCGA#occurances', max_length=20, null=True)
    oncokb = models.CharField(verbose_name='oncoKB', max_length=500, null=True)
    oncokb_pmids = models.CharField(verbose_name='oncoKB_PMIDs', max_length=50, null=True)
    watson = models.CharField(max_length=20, null=True)
    watson_pmids = models.CharField(verbose_name='Watson_PMIDs', max_length=50, null=True)
    qci = models.CharField(verbose_name='QCI', max_length=20, null=True)
    qci_pmids = models.CharField(verbose_name='QCI_PMIDs', max_length=50, null=True)
    jaxckb = models.CharField(verbose_name='JaxCKB', max_length=10, null=True)
    jaxckb_pmids = models.CharField(verbose_name='JaxCKB_PMIDs', max_length=50, null=True)
    pmkb = models.CharField(verbose_name='PMKB', max_length=10, null=True)
    pmkb_citations = models.CharField(verbose_name='PMKB_citations', max_length=500, null=True)
    civic = models.CharField(verbose_name='CIViC', max_length=50, null=True)
    google = models.CharField(max_length=100, null=True)
    alamut = models.CharField(max_length=70, null=True)
    gene = models.ForeignKey(Gene, related_name='variants', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.protein


class CancerHotspot(models.Model):
    hotspot = models.CharField(max_length=70, null=True)
    count = models.IntegerField(default=1)
    variant = models.ForeignKey(Variant, related_name='hotspots', on_delete=models.CASCADE, null=True, blank=True)


class PathItem(models.Model):
    key = models.CharField(max_length=5, null=True)
    content = models.CharField(max_length=75, null=True)
    value = models.IntegerField(default=0)

    def __str__(self):
        return self.key


class Disease(models.Model):
    name = models.CharField(max_length=20, null=True)
    branch = models.CharField(choices=BRANCH_CHOICES, max_length=2, default='so')
    others = models.CharField(choices=TIER_CHOICES, max_length=20, null=True)
    report = models.CharField(max_length=20, null=True)
    variant = models.ForeignKey(Variant, related_name='diseases', on_delete=models.CASCADE, null=True, blank=True)
    reviewed = models.CharField(choices=(
        ('n', 'Not Reviewed'),
        ('r', 'Reviewed'),
        ('m', 'Secondly Reviewed'),
        ('a', 'Approved'),
    ), max_length=1, default='n')
    reviewed_date = models.DateTimeField('reviewed date', null=True)
    review_user = models.ForeignKey(User, related_name='reviewed_variants', on_delete=models.CASCADE, null=True, blank=True)
    meta_reviewed_date = models.DateTimeField('meta-reviewed date', null=True)
    meta_review_user = models.ForeignKey(User, related_name='meta_reviewed_variants', on_delete=models.CASCADE, null=True, blank=True)
    approved_date = models.DateTimeField('approved date', null=True)
    approve_user = models.ForeignKey(User, related_name='approved_variants', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Score(models.Model):
    for_score = models.CharField(max_length=20, null=True)
    against_score = models.CharField(max_length=20, null=True)
    content = models.CharField(max_length=100, null=True)


class DxToScore(models.Model):
    disease = models.OneToOneField(Disease, on_delete=models.CASCADE, related_name='disease', null=True, blank=True)
    score = models.OneToOneField(Disease, on_delete=models.CASCADE, null=True, blank=True)


class Functional(models.Model):
    key = models.CharField(
        choices=FUNC_SIG_CHOICES, max_length=20,
        null=True,
    )
    value = models.CharField(
        choices=FUNC_CAT_CHOICES,
        max_length=20,
        null=True
    )
    disease = models.ForeignKey(Disease, related_name='functionals', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.key


class Evidence(models.Model):
    item = models.ForeignKey(PathItem, on_delete=models.CASCADE, null=True, blank=True)
    functional = models.ForeignKey(Functional, related_name='evidences', on_delete=models.CASCADE, null=True, blank=True)
    disease = models.ForeignKey(Disease, related_name='evidences', on_delete=models.CASCADE, null=True, blank=True)
    source_type = models.CharField(
        max_length=2,
        choices=TYPE_CHOICES,
        default='PM',
    )
    source_id = models.CharField(max_length=20, null=True)
    statement = models.TextField(null=True)

    def __str__(self):
        if self.item:
            return self.item.key
        elif self.functional:
            return self.functional.value
        else:
            return self.statement


class SubEvidence(models.Model):
    evid_sig = models.CharField(
        max_length=4,
        choices=EVID_SIG_CHOICES,
        default='Pred',
    )
    level = models.CharField(
        max_length=1,
        choices=EVID_LEVEL_CHOICES,
        null=True
    )
    evid_dir = models.BooleanField(
        choices=EVID_DIR_CHOICES,
        null=True
    )
    clin_sig = models.CharField(
        choices=CLIN_SIG_CHOICES,
        max_length=25
    )
    drug_class = models.TextField(null=True)
    evid_rating = models.IntegerField(
        choices=EVID_RATING_CHOICES,
        default=1
    )
    evidence = models.ForeignKey(Evidence, related_name='subevidences', on_delete=models.CASCADE, null=True, blank=True)
    variant = models.ForeignKey(Variant, related_name='subevidences', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.clin_sig


class Report(models.Model):
    name = models.CharField(max_length=40)
    content = models.TextField(null=True)
    gene = models.ForeignKey(Gene, related_name='reports', on_delete=models.CASCADE, null=True, blank=True)
    variant = models.ForeignKey(Variant, related_name='reports', on_delete=models.CASCADE, null=True, blank=True)
    disease = models.ForeignKey(Disease, related_name='reports', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.content


class History(models.Model):
    content = models.TextField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    object = models.ForeignKey(Evidence, verbose_name='field', related_name='histories', on_delete=models.CASCADE, null=True, blank=True)
    variant = models.ForeignKey(Variant, related_name='history', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return str(self.user) + ' / ' + self.timestamp.strftime('%Y-%m-%d')


# TODO: Delete Class
class Interpretation(models.Model):
    content = models.TextField(blank=True)
    genes = models.ManyToManyField(Gene, related_name='interpretations')
    variants = models.ManyToManyField(Variant, related_name='interpretations')
