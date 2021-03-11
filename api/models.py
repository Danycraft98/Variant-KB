from django.db import models

from accounts.models import User
from .constants import *

__all__ = [
    'Gene', 'Variant', 'Disease', 'History', 'CancerHotspot', 'PathItem', 'Score', 'Functional',
    'Evidence', 'SubEvidence', 'Report', 'ITEMS'
]


class Gene(models.Model):
    """
    A class used to represent a Gene object

    Attributes:
        name (models.CharField): Gene name
        pub_date (models.DateTimeField): Date published
        content (models.TextField): Gene-Descriptive report
        germline_content (models.TextField): Gene-Germline report
    """
    name = models.CharField(max_length=20)
    pub_date = models.DateTimeField('date published')
    content = models.TextField(null=True, blank=True)
    germline_content = models.TextField(null=True, blank=True)

    def __str__(self):
        """
        The string return method

        Returns: str
        """
        return self.name

    @staticmethod
    def class_type():
        """
        The class type return method

        Returns: str
        """
        return 'Gene'


class Variant(models.Model):
    """ A class used to represent a Variant object """
    genome_build = models.CharField(verbose_name='genome build', max_length=10, null=True, blank=True)
    chr = models.CharField(verbose_name='Chromosome', max_length=6, null=True, blank=True)
    start = models.CharField(max_length=10, null=True, blank=True)
    end = models.CharField(max_length=10, null=True, blank=True)
    ref = models.CharField(max_length=100, null=True, blank=True)
    alt = models.CharField(max_length=100, null=True, blank=True)
    transcript = models.CharField(max_length=20)
    cdna = models.CharField(verbose_name='c.', max_length=10, null=True, blank=True)
    protein = models.CharField(verbose_name='p.', max_length=20)
    consequence = models.CharField(max_length=10, null=True, blank=True)
    exonic_function = models.CharField(max_length=20, null=True, blank=True)
    content = models.TextField(blank=True)
    germline_content = models.TextField(blank=True)

    af = models.CharField(verbose_name='AF', max_length=20, null=True, blank=True)
    af_popmax = models.CharField(verbose_name='AF_popmax', max_length=20, null=True, blank=True)
    cosmic70 = models.CharField(max_length=20, null=True, blank=True)
    clinvar = models.CharField(verbose_name='CLINVAR', max_length=20, null=True, blank=True)
    insilicodamaging = models.CharField(verbose_name='InSilicoDamaging', max_length=20, null=True, blank=True)
    insilicobenign = models.CharField(verbose_name='InSilicoBenign', max_length=100, null=True, blank=True)
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
    tcga = models.CharField(verbose_name='TCGA#occurances', max_length=20, null=True, blank=True)
    oncokb = models.CharField(verbose_name='oncoKB', max_length=500, null=True, blank=True)
    oncokb_pmids = models.CharField(verbose_name='oncoKB_PMIDs', max_length=50, null=True, blank=True)
    watson = models.CharField(max_length=20, null=True, blank=True)
    watson_pmids = models.CharField(verbose_name='Watson_PMIDs', max_length=50, null=True, blank=True)
    qci = models.CharField(verbose_name='QCI', max_length=20, null=True, blank=True)
    qci_pmids = models.CharField(verbose_name='QCI_PMIDs', max_length=50, null=True, blank=True)
    jaxckb = models.CharField(verbose_name='JaxCKB', max_length=10, null=True, blank=True)
    jaxckb_pmids = models.CharField(verbose_name='JaxCKB_PMIDs', max_length=50, null=True, blank=True)
    pmkb = models.CharField(verbose_name='PMKB', max_length=10, null=True, blank=True)
    pmkb_citations = models.CharField(verbose_name='PMKB_citations', max_length=500, null=True, blank=True)
    civic = models.CharField(verbose_name='CIViC', max_length=50, null=True, blank=True)
    google = models.CharField(max_length=100, null=True, blank=True)
    alamut = models.CharField(max_length=70, null=True, blank=True)
    gene = models.ForeignKey(Gene, related_name='variants', on_delete=models.CASCADE)

    def __str__(self):
        """
        The string return method

        Returns: str
        """
        return self.protein


class CancerHotspot(models.Model):
    """ A class used to represent a Cancer hotspot object """
    hotspot = models.CharField(max_length=70, null=True, blank=True)
    count = models.IntegerField(default=1, null=True, blank=True)
    variant = models.ForeignKey(Variant, related_name='hotspots', on_delete=models.CASCADE)


class PathItem(models.Model):
    """ A class used to represent a Path item object """
    key = models.CharField(max_length=5, null=True, blank=True)
    content = models.CharField(max_length=75, null=True, blank=True)
    value = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        """
        The string return method

        Returns: str
        """
        return self.key


class Disease(models.Model):
    """ A class used to represent a Disease object """
    name = models.CharField(max_length=20)
    branch = models.CharField(choices=BRANCH_CHOICES, max_length=2, default='no')
    others = models.CharField(choices=TIER_CHOICES, max_length=20, null=True, blank=True)
    report = models.TextField(verbose_name='Germline Report', max_length=255, null=True, blank=True)
    variant = models.ForeignKey(Variant, related_name='diseases', on_delete=models.CASCADE)
    reviewed = models.CharField(choices=REVIEWED_CHOICES, max_length=1, default='n')
    reviewed_date = models.DateTimeField('reviewed date', null=True, blank=True)
    review_user = models.ForeignKey(User, related_name='reviewed_variants', on_delete=models.CASCADE, null=True, blank=True)
    meta_reviewed_date = models.DateTimeField('meta-reviewed date', null=True, blank=True)
    meta_review_user = models.ForeignKey(User, related_name='meta_reviewed_variants', on_delete=models.CASCADE, null=True, blank=True)
    approved_date = models.DateTimeField('approved date', null=True, blank=True)
    approve_user = models.ForeignKey(User, related_name='approved_variants', on_delete=models.CASCADE, null=True, blank=True)
    curation_notes = models.TextField(verbose_name='Curation Notes', max_length=255, null=True, blank=True)

    def __str__(self):
        """
        The string return method

        Returns: str
        """
        return self.name


class Score(models.Model):
    """ A class used to represent a Score object """
    for_score = models.CharField(verbose_name='For Pathogenicity', max_length=20)
    against_score = models.CharField(verbose_name='Against Pathogenicity', max_length=20)
    content = models.CharField(verbose_name='ACMG Classification', max_length=100)
    disease = models.OneToOneField(Disease, on_delete=models.CASCADE, related_name='score')

    def __str__(self):
        """
        The string return method

        Returns: str
        """
        return self.for_score + ' ' + self.against_score + '\n' + self.content


class Functional(models.Model):
    """ A class used to represent a Functional object """
    key = models.CharField(verbose_name='Functional Significance', choices=FUNC_SIG_CHOICES, max_length=20, blank=True, null=True)
    value = models.CharField(verbose_name='Functional Class', choices=FUNC_CAT_CHOICES, max_length=20, blank=True, null=True)
    disease = models.ForeignKey(Disease, related_name='functionals', on_delete=models.CASCADE)

    def __str__(self):
        """
        The string return method

        Returns: str
        """
        return self.key


class Evidence(models.Model):
    """ A class used to represent a Evidence object """
    item = models.ForeignKey(PathItem, on_delete=models.CASCADE, null=True, blank=True)
    functional = models.ForeignKey(Functional, related_name='evidences', on_delete=models.CASCADE, null=True, blank=True)
    disease = models.ForeignKey(Disease, related_name='evidences', on_delete=models.CASCADE, null=True, blank=True)
    source_type = models.CharField(
        max_length=2,
        choices=TYPE_CHOICES,
        default='PM',
        null=True,
        blank=True
    )
    source_id = models.CharField(max_length=20, null=True, blank=True)
    statement = models.TextField(null=True, blank=True, default='')

    def __str__(self):
        """
        The string return method

        Returns: str
        """
        if self.item:
            return self.item.key
        elif self.functional:
            return self.functional.value
        else:
            return self.statement


class SubEvidence(models.Model):
    """ A class used to represent a SubEvidence object """
    evid_sig = models.CharField(
        verbose_name='Evidence Significance',
        max_length=4,
        choices=EVID_SIG_CHOICES,
        default='Pred',
        null=True,
        blank=True
    )
    level = models.CharField(
        verbose_name='Evidence Level',
        max_length=1,
        choices=EVID_LEVEL_CHOICES,
        null=True,
        blank=True
    )
    evid_dir = models.BooleanField(
        verbose_name='Evidence Direction',
        choices=EVID_DIR_CHOICES,
        null=True,
        blank=True
    )
    clin_sig = models.CharField(
        verbose_name='Clinical Significance',
        choices=CLIN_SIG_CHOICES,
        max_length=25,
        null=True,
        blank=True
    )
    drug_class = models.TextField(
        verbose_name='Drug/Drug Class/Dx',
        null=True,
        blank=True
    )
    evid_rating = models.IntegerField(
        verbose_name='Evidence Rating',
        choices=EVID_RATING_CHOICES,
        default=1,
        null=True,
        blank=True
    )
    evidence = models.ForeignKey(Evidence, related_name='subevidences', on_delete=models.CASCADE, null=True, blank=True)
    variant = models.ForeignKey(Variant, related_name='subevidences', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        """
        The string return method

        Returns: str
        """
        return self.evidence


class Report(models.Model):
    report_name = models.CharField(max_length=40)
    content = models.TextField(null=True)
    gene = models.ForeignKey(Gene, related_name='reports', on_delete=models.CASCADE, null=True, blank=True)
    variant = models.ForeignKey(Variant, related_name='reports', on_delete=models.CASCADE, null=True, blank=True)
    disease = models.ForeignKey(Disease, related_name='reports', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        """
        The string return method

        Returns: str
        """
        return self.content


class History(models.Model):
    """ A class used to represent a History object """
    content = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    object = models.ForeignKey(Evidence, verbose_name='field', related_name='histories', on_delete=models.CASCADE, null=True, blank=True)
    variant = models.ForeignKey(Variant, related_name='history', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        """
        Order by timestamp
        """
        ordering = ['timestamp']

    def __str__(self):
        """
        The string return method

        Returns: str
        """
        return str(self.user) + ' / ' + self.timestamp.strftime('%Y-%m-%d')
