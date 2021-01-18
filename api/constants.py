# Constants
BRANCH_CHOICES = [
    ('gp', 'Germline Pathogenecity'),
    ('so', 'Somatic Oncogenecity')
]

ITEMS = {  # 'PVS1 - SA': ['Stand Alone - whole gene deletion', 10],
    'PVS1': ['nonsense, fs, +/-2 splice site, start loss, whole exon deletion', 10],

    'PS1': ['same aa change as previously published, intragenic exon duplication', 7],
    'PS2': ['confirmed de novo, no FHx (rarely applied)', 7],
    'PS3': ['well-established functional studies', 7],
    'PS4': ['prevalence affected >>> controls (case control studies)', 7],

    'PM': ['previously reported in affected, not in controls', 2],
    'PM1': ['mutational hot spot, functional domain (rarely applied)', 2],
    'PM2': ['absent from or low freq in controls (gnomAD)', 2],
    'PM3': ['in trans with pathogenic in recessive disorder (rarely applied)', 2],
    'PM4': ['altered protein length (in-frame nonrepeat or stop loss; rarely applied)', 2],
    'PM5': ['novel aa at previously reported pathogenic codon', 2],
    'PM6': ['assumed de novo (rarely applied)', 2],

    'PP1': ['cosegregation in multiple family members (rarely applied)', 1],
    'PP2': ['missense in rarely mutated gene; missense = mechanism (rarely applied)', 1],
    'PP3': ['in silico prediction', 1],
    'PP4': ['phenotype or FHx is highly specific for a disorder (rarely applied)', 1],
    'PP5': ['reputable source (e.g. ClinVar, LSDB, etc.)', 1],

    'BA1': ['common polymorphism; allele frequency > 5%', 16],

    'BS1': ['allele frequency > expected (HW equilibrium)', 8],
    'BS2': ['observed in healthy adult (assuming full penetrance; rarely applied)', 8],
    'BS3': ['well-established functional studies', 8],
    'BS4': ['lack of segregation in affected family members', 8],

    'BP1': ['missense when truncating variants are deleterious (rarely applied)', 1],
    'BP2': ['in trans with pathogenic in AD or cis with pathogenic AD/AR', 1],
    'BP3': ['in-frame del/ins in repetitive region w/o known function (rarely applied)', 1],
    'BP4': ['in silico prediction', 1], 'BP5': ['in case with alternate basis for disease', 1],
    'BP6': ['reputable source', 1], 'BP7': ['synonymous variant (not splice)', 1]}

FUNC_SIG_CHOICES = [
    (None, 'Select',),
    ('Established', 'Established Significance'),
    ('Likely', 'Likely Significance'),
    ('Predicted', 'Predicted/Possible Significance'),
    ('VUS', 'Uncertain Significance'),
    ('Benign', 'Benign')
]

FUNC_CAT_CHOICES = [
    (None, 'Select',),
    ('GOF', 'GOF'),
    ('LOF', 'LOF'),
    ('TP53 functional', 'TP53 functional'),
    ('TP53 non-functional', 'TP53 non-functional'),
    ('BRAF Class I', 'BRAF Class I'),
    ('BRAF Class II', 'BRAF Class II'),
    ('BRAF Class III', 'BRAF Class III')
]

TIER_CHOICES = [
    (None, 'Select',),
    ('Tier I', 'Tier I'),
    ('Tier II', 'Tier II'),
    ('Tier III', 'Tier III'),
    ('Tier IV', 'Tier IV')
]

TYPE_CHOICES = [
    ('PM', 'PMID'),
    ('O', 'Others')
]

EVID_SIG_CHOICES = [
    (None, 'Select',),
    ('Pred', 'Predictive'),
    ('Prog', 'Prognostic'),
    ('Diag', 'Diagnostic')
]

EVID_LEVEL_CHOICES = [
    (None, 'Select',),
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D'),
    ('E', 'E')
]

EVID_DIR_CHOICES = [
    (None, 'Select',),
    (True, 'Support'),
    (False, 'Does Not Support')
]

CLIN_SIG_CHOICES = [
    (None, 'Select',),
    ('Pred: Resistance', 'Pred: Resistance'),
    ('Pred: Adverse Response', 'Pred: Adverse Response'),
    ('Pred: Reduced Sensitivity', 'Pred: Reduced Sensitivity'),
    ('Pred: Sensitivity', 'Pred: Sensitivity'),
    ('Prog: Better Outcome', ' disabled hidden> Prog: Better Outcome'),
    ('Prog: Poorer Outcome', ' disabled hidden> Prog: Poorer Outcome'),
    ('Dx: Positive Diagnosis', ' disabled hidden> Dx: Positive Diagnosis'),
    ('Dx: Negative Diagnosis', ' disabled hidden> Dx: Negative Diagnosis')
]

EVID_RATING_CHOICES = [
    (0, 'Select',),
    (1, '1 Star'),
    (2, '2 Stars'),
    (3, '3 Stars'),
    (4, '4 Stars'),
    (5, '5 Stars'),
]
