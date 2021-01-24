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
    """
    A class used to represent a Variant object

    Attributes:
        genome_build (models.CharField): Gemone Build
        chr (models.CharField): Chromosome
        start (models.CharField): Chromosome start index
        end (models.CharField): Chromosome end index
        ref (models.CharField): Chromosome ref sequence
        alt (models.CharField): Chromosome alf sequence
        transcript (models.CharField): Variant transcript
        cdna (models.CharField): cDNA
        protein (models.CharField): Variant protein
            consequence (models.CharField): Variant Consequence (?)
        exonic_function (models.CharField): Variant Exonic Function
        content (models.TextField): Variant-Descriptive Report
        germline_content (models.TextField): Variant-Germline Report

        af (models.CharField): AF
        af_popmax (models.CharField): AF_popmax
        cosmic70 (models.CharField): COSMIC70
        clinvar (models.CharField): CLINVAR
        insilicodamaging (models.CharField): InSilicoDamaging
        insilicobenign (models.CharField): InSilicoBenign
        polyphen2_hdiv_pred (models.CharField): Polyphen2_HDIV_pred
        polyphen2_hvar_pred (models.CharField): Polyphen2_HVAR_pred
        sift_pred (models.CharField): SIFT_pred
        mutationtaster_pred (models.CharField): MutationTaster_pred
        mutationassessor_pred (models.CharField): MutationAssessor_pred
        provean_pred (models.CharField): PROVEAN_pred
            lrt_pred (models.CharField): PROVEAN_pred?
        tcga (models.CharField): TCGA#occurances
        oncokb (models.CharField): oncoKB
        oncokb_pmids (models.CharField): oncoKB_PMIDs'
        watson (models.CharField): Watson
        watson_pmids (models.CharField): Watson_PMIDs
        qci (models.CharField): QCI
        qci_pmids (models.CharField): QCI_PMIDs
        jaxckb (models.CharField): JaxCKB
        jaxckb_pmids (models.CharField): JaxCKB_PMIDs
        pmkb (models.CharField): PMKB
        pmkb_citations (models.CharField): PMKB_citations
        civic (models.CharField): CIViC
        google (models.CharField): Google Link
        alamut (models.CharField): Alamut Link
        gene (models.ForeignKey): Gene object
    """
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
    gene = models.ForeignKey(Gene, related_name='variants', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        """
        The string return method

        Returns: str
        """
        return self.protein


class CancerHotspot(models.Model):
    """
    A class used to represent a Cancer hotspot object

    Attributes:
        hotspot (models.CharField): Cancer hotspot name
        count (models.IntegerField): Cancer hotspot count value
        variant (models.ForeignKey): Variant object
    """
    hotspot = models.CharField(max_length=70, null=True, blank=True)
    count = models.IntegerField(default=1, null=True, blank=True)
    variant = models.ForeignKey(Variant, related_name='hotspots', on_delete=models.CASCADE, null=True, blank=True)


class PathItem(models.Model):
    """
    A class used to represent a Path item object

    Attributes:
        key (models.CharField): Path item name
        value (models.IntegerField): Path item score value
        content (models.CharField): Path item description
    """
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
    """
    A class used to represent a Disease object

    Attributes:
        name (models.CharField): Disease name
        branch (models.CharField): Disease branch
        others (models.CharField): Disease tier
        report (models.CharField): Disease report
        variant (models.ForeignKey): Variant object
        reviewed (models.CharField): Disease reviewed status
        reviewed_date (models.DateTimeField): Disease reviewed date
        review_user (models.ForeignKey): Disease review user
        meta_reviewed_date (models.DateTimeField): Disease meta-reviewed date
        meta_review_user (models.ForeignKey): Disease meta-reviewe user
        approved_date (models.DateTimeField): Disease approved date
        approve_user (models.ForeignKey): Disease approve user
    """
    name = models.CharField(max_length=20)
    branch = models.CharField(choices=BRANCH_CHOICES, max_length=2, default='no')
    others = models.CharField(choices=TIER_CHOICES, max_length=20, null=True, blank=True)
    report = models.CharField(verbose_name='Germline Report', max_length=20, null=True, blank=True)
    variant = models.ForeignKey(Variant, related_name='diseases', on_delete=models.CASCADE, null=True, blank=True)
    reviewed = models.CharField(choices=REVIEWED_CHOICES, max_length=1, default='n')
    reviewed_date = models.DateTimeField('reviewed date', null=True, blank=True)
    review_user = models.ForeignKey(User, related_name='reviewed_variants', on_delete=models.CASCADE, null=True, blank=True)
    meta_reviewed_date = models.DateTimeField('meta-reviewed date', null=True, blank=True)
    meta_review_user = models.ForeignKey(User, related_name='meta_reviewed_variants', on_delete=models.CASCADE, null=True, blank=True)
    approved_date = models.DateTimeField('approved date', null=True, blank=True)
    approve_user = models.ForeignKey(User, related_name='approved_variants', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        """
        The string return method

        Returns: str
        """
        return self.name


class Score(models.Model):
    """
    A class used to represent a Score object

    Attributes:
        for_score (models.CharField): Score ACMG for score
        against_score (models.CharField): Score ACMG against score
        content (models.CharField): Score ACMG classification
        disease (models.OneToOneField): Disease object
    """
    for_score = models.CharField(verbose_name='For Pathogenicity', max_length=20, null=True, blank=True)
    against_score = models.CharField(verbose_name='Against Pathogenicity', max_length=20, null=True, blank=True)
    content = models.CharField(verbose_name='ACMG Classification', max_length=100, null=True, blank=True)
    disease = models.OneToOneField(Disease, on_delete=models.CASCADE, related_name='score', null=True, blank=True)

    def __str__(self):
        """
        The string return method

        Returns: str
        """
        return self.for_score + ' ' + self.against_score + '\n' + self.content


class Functional(models.Model):
    """
    A class used to represent a Functional object

    Attributes:
        key (models.CharField): Functional Significance
        value (models.CharField): Functional Category
        disease (models.OneToOneField): Disease object
    """
    key = models.CharField(
        verbose_name='Functional Significance',
        choices=FUNC_SIG_CHOICES, max_length=20,
        null=True,
        blank=True
    )
    value = models.CharField(
        verbose_name='Functional Class',
        choices=FUNC_CAT_CHOICES,
        max_length=20,
        null=True,
        blank=True
    )
    disease = models.ForeignKey(Disease, related_name='functionals', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        """
        The string return method

        Returns: str
        """
        return self.key


class Evidence(models.Model):
    """
    A class used to represent a Evidence object

    Attributes:
        item (models.ForeignKey): PathItem object
        functional (models.ForeignKey): Functional object
        disease (models.ForeignKey): Disease object
        source_type (models.CharField): Evidence source type
        source_id (models.CharField): Evidence source ID
        statement (models.CharField): Evidence statement
    """
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
    statement = models.TextField(null=True)

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
    """
    A class used to represent a SubEvidence object

    Attributes:
        evid_sig (models.CharField): Evidence Significance
        level (models.CharField): Evidence Level
        evid_dir (models.CharField): Evidence Direction
        clin_sig (models.CharField): Clinial Significance
        drug_class (models.CharField): Drug/Drug Class/Dx
        evid_rating (models.CharField): Evidence Rating
        evidence (models.ForeignKey): Evidence object
        variant (models.ForeignKey): Variant object
    """
    evid_sig = models.CharField(
        verbose_name='Evidence Significance',
        max_length=4,
        choices=EVID_SIG_CHOICES,
        default='Pred',
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
        max_length=25
    )
    drug_class = models.TextField(
        verbose_name='Drug/Drug Class/Dx',
        null=True,
        blank=True
    )
    evid_rating = models.IntegerField(
        verbose_name='Evidence Rating',
        choices=EVID_RATING_CHOICES,
        default=1
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
    name = models.CharField(max_length=40)
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
    """
    A class used to represent a History object

    Attributes:
        content (models.CharField): History content
        timestamp (models.CharField): History timestamp
        user (models.ForeignKey): User object
        object (models.ForeignKey): Evidence object
        variant (models.ForeignKey): Variant object
    """
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
