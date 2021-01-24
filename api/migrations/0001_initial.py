import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

from api.models import ITEMS


def add_path_items(apps, _schema_editor):
    """
    apps: ? Used; to get apps
    _schema_editor: ?; not used parameter
    return:

    Initialize PathItem models.
    """
    PathItem = apps.get_model('api', 'PathItem')
    for key, value in ITEMS.items():
        PathItem.objects.get_or_create(key=key, value=value[1], content=value[0])


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Disease',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('branch', models.CharField(choices=[('no', 'No Disease'), ('gp', 'Germline Pathogenicity'), ('so', 'Somatic Oncogenicity')], default='no', max_length=2)),
                ('others', models.CharField(blank=True, choices=[(None, 'Select'), ('Tier I', 'Tier I'), ('Tier II', 'Tier II'), ('Tier III', 'Tier III'), ('Tier IV', 'Tier IV')], max_length=20, null=True)),
                ('report', models.CharField(blank=True, max_length=20, null=True, verbose_name='Germline Report')),
                ('reviewed', models.CharField(choices=[('n', 'Not Reviewed'), ('r', 'Reviewed'), ('m', 'Secondly Reviewed'), ('a', 'Approved')], default='n', max_length=1)),
                ('reviewed_date', models.DateTimeField(blank=True, null=True, verbose_name='reviewed date')),
                ('meta_reviewed_date', models.DateTimeField(blank=True, null=True, verbose_name='meta-reviewed date')),
                ('approved_date', models.DateTimeField(blank=True, null=True, verbose_name='approved date')),
                ('approve_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='approved_variants', to=settings.AUTH_USER_MODEL)),
                ('meta_review_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='meta_reviewed_variants', to=settings.AUTH_USER_MODEL)),
                ('review_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviewed_variants', to=settings.AUTH_USER_MODEL)),
            ],
        ),

        migrations.CreateModel(
            name='Evidence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_type', models.CharField(blank=True, choices=[('PM', 'PMID'), ('O', 'Others')], default='PM', max_length=2, null=True)),
                ('source_id', models.CharField(blank=True, max_length=20, null=True)),
                ('statement', models.TextField(null=True)),
                ('disease', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='evidences', to='api.disease')),
            ],
        ),

        migrations.CreateModel(
            name='Gene',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('content', models.TextField(blank=True, null=True)),
                ('germline_content', models.TextField(blank=True, null=True)),
            ],
        ),

        migrations.CreateModel(
            name='PathItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(blank=True, max_length=5, null=True)),
                ('content', models.CharField(blank=True, max_length=75, null=True)),
                ('value', models.IntegerField(blank=True, default=0, null=True)),
            ],
        ),

        migrations.CreateModel(
            name='Variant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genome_build', models.CharField(blank=True, max_length=10, null=True, verbose_name='genome build')),
                ('chr', models.CharField(blank=True, max_length=6, null=True, verbose_name='Chromosome')),
                ('start', models.CharField(blank=True, max_length=10, null=True)),
                ('end', models.CharField(blank=True, max_length=10, null=True)),
                ('ref', models.CharField(blank=True, max_length=100, null=True)),
                ('alt', models.CharField(blank=True, max_length=100, null=True)),
                ('transcript', models.CharField(max_length=20)),
                ('cdna', models.CharField(blank=True, max_length=10, null=True, verbose_name='c.')),
                ('protein', models.CharField(max_length=20, verbose_name='p.')),
                ('consequence', models.CharField(blank=True, max_length=10, null=True)),
                ('exonic_function', models.CharField(blank=True, max_length=20, null=True)),
                ('content', models.TextField(blank=True)),
                ('germline_content', models.TextField(blank=True)),
                ('af', models.CharField(blank=True, max_length=20, null=True, verbose_name='AF')),
                ('af_popmax', models.CharField(blank=True, max_length=20, null=True, verbose_name='AF_popmax')),
                ('cosmic70', models.CharField(blank=True, max_length=20, null=True)),
                ('clinvar', models.CharField(blank=True, max_length=20, null=True, verbose_name='CLINVAR')),
                ('insilicodamaging', models.CharField(blank=True, max_length=20, null=True, verbose_name='InSilicoDamaging')),
                ('insilicobenign', models.CharField(blank=True, max_length=100, null=True, verbose_name='InSilicoBenign')),
                ('polyphen2_hdiv_pred', models.CharField(choices=[('D', 'probably damaging'), ('P', 'possibly damaging'), ('B', 'benign'), ('na', 'na')], default='na', max_length=2, verbose_name='Polyphen2_HDIV_pred')),
                ('polyphen2_hvar_pred', models.CharField(choices=[('D', 'probably damaging'), ('P', 'possibly damaging'), ('B', 'benign'), ('na', 'na')], default='na', max_length=2, verbose_name='Polyphen2_HVAR_pred')),
                ('sift_pred', models.CharField(choices=[('D', 'deleterious'), ('T', 'tolerated'), ('na', 'na')], default='na', max_length=2, verbose_name='SIFT_pred')),
                ('mutationtaster_pred', models.CharField(choices=[('D', 'deleterious'), ('T', 'tolerated'), ('na', 'na')], default='na', max_length=2, verbose_name='MutationTaster_pred')),
                ('mutationassessor_pred', models.CharField(choices=[('H', 'high'), ('M', 'medium'), ('L', 'low'), ('N', 'neutral'), ('na', 'na')], default='na', max_length=2, verbose_name='MutationAssessor_pred')),
                ('provean_pred', models.CharField(choices=[('D', 'deleterious'), ('N', 'neutral'), ('na', 'na')], default='na', max_length=2, verbose_name='PROVEAN_pred')),
                ('lrt_pred', models.CharField(choices=[('D', 'deleterious'), ('N', 'neutral'), ('U', 'unknown'), ('na', 'na')], default='na', max_length=2, verbose_name='PROVEAN_pred')),
                ('tcga', models.CharField(blank=True, max_length=20, null=True, verbose_name='TCGA#occurances')),
                ('oncokb', models.CharField(blank=True, max_length=500, null=True, verbose_name='oncoKB')),
                ('oncokb_pmids', models.CharField(blank=True, max_length=50, null=True, verbose_name='oncoKB_PMIDs')),
                ('watson', models.CharField(blank=True, max_length=20, null=True)),
                ('watson_pmids', models.CharField(blank=True, max_length=50, null=True, verbose_name='Watson_PMIDs')),
                ('qci', models.CharField(blank=True, max_length=20, null=True, verbose_name='QCI')),
                ('qci_pmids', models.CharField(blank=True, max_length=50, null=True, verbose_name='QCI_PMIDs')),
                ('jaxckb', models.CharField(blank=True, max_length=10, null=True, verbose_name='JaxCKB')),
                ('jaxckb_pmids', models.CharField(blank=True, max_length=50, null=True, verbose_name='JaxCKB_PMIDs')),
                ('pmkb', models.CharField(blank=True, max_length=10, null=True, verbose_name='PMKB')),
                ('pmkb_citations', models.CharField(blank=True, max_length=500, null=True, verbose_name='PMKB_citations')),
                ('civic', models.CharField(blank=True, max_length=50, null=True, verbose_name='CIViC')),
                ('google', models.CharField(blank=True, max_length=100, null=True)),
                ('alamut', models.CharField(blank=True, max_length=70, null=True)),
                ('gene', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='variants', to='api.gene')),
            ],
        ),

        migrations.CreateModel(
            name='SubEvidence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('evid_sig', models.CharField(choices=[(None, 'Select'), ('Pred', 'Predictive'), ('Prog', 'Prognostic'), ('Diag', 'Diagnostic')], default='Pred', max_length=4, verbose_name='Evidence Significance')),
                ('level', models.CharField(blank=True, choices=[(None, 'Select'), ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E')], max_length=1, null=True, verbose_name='Evidence Level')),
                ('evid_dir', models.BooleanField(blank=True, choices=[(None, 'Select'), (True, 'Support'), (False, 'Does Not Support')], null=True, verbose_name='Evidence Direction')),
                ('clin_sig', models.CharField(choices=[(None, 'Select'), ('Pred: Resistance', 'Pred: Resistance'), ('Pred: Adverse Response', 'Pred: Adverse Response'), ('Pred: Reduced Sensitivity', 'Pred: Reduced Sensitivity'), ('Pred: Sensitivity', 'Pred: Sensitivity'),
                                                       ('Prog: Better Outcome', ' disabled hidden> Prog: Better Outcome'), ('Prog: Poorer Outcome', ' disabled hidden> Prog: Poorer Outcome'), ('Dx: Positive Diagnosis', ' disabled hidden> Dx: Positive Diagnosis'),
                                                       ('Dx: Negative Diagnosis', ' disabled hidden> Dx: Negative Diagnosis')], max_length=25, verbose_name='Clinical Significance')),
                ('drug_class', models.TextField(blank=True, null=True, verbose_name='Drug/Drug Class/Dx')),
                ('evid_rating', models.IntegerField(choices=[(0, 'Select'), (1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')], default=1, verbose_name='Evidence Rating')),
                ('evidence', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subevidences', to='api.evidence')),
                ('variant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subevidences', to='api.variant')),
            ],
        ),

        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('for_score', models.CharField(blank=True, max_length=20, null=True, verbose_name='For Pathogenicity')),
                ('against_score', models.CharField(blank=True, max_length=20, null=True, verbose_name='Against Pathogenicity')),
                ('content', models.CharField(blank=True, max_length=100, null=True, verbose_name='ACMG Classification')),
                ('disease', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='score', to='api.disease')),
            ],
        ),

        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('content', models.TextField(null=True)),
                ('disease', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='api.disease')),
                ('gene', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='api.gene')),
                ('variant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='api.variant')),
            ],
        ),

        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('object', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='histories', to='api.evidence', verbose_name='field')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('variant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='history', to='api.variant')),
            ],
            options={
                'ordering': ['timestamp'],
            },
        ),

        migrations.CreateModel(
            name='Functional',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(blank=True, choices=[(None, 'Select'), ('Established', 'Established Significance'), ('Likely', 'Likely Significance'), ('Predicted', 'Predicted/Possible Significance'), ('VUS', 'Uncertain Significance'), ('Benign', 'Benign')], max_length=20, null=True,
                                         verbose_name='Functional Significance')),
                ('value', models.CharField(blank=True,
                                           choices=[(None, 'Select'), ('GOF', 'GOF'), ('LOF', 'LOF'), ('TP53 functional', 'TP53 functional'), ('TP53 non-functional', 'TP53 non-functional'), ('BRAF Class I', 'BRAF Class I'), ('BRAF Class II', 'BRAF Class II'), ('BRAF Class III', 'BRAF Class III')],
                                           max_length=20, null=True, verbose_name='Functional Class')),
                ('disease', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='functionals', to='api.disease')),
            ],
        ),

        migrations.AddField(
            model_name='evidence',
            name='functional',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='evidences', to='api.functional'),
        ),

        migrations.AddField(
            model_name='evidence',
            name='item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.pathitem'),
        ),

        migrations.AddField(
            model_name='disease',
            name='variant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='diseases', to='api.variant'),
        ),

        migrations.CreateModel(
            name='CancerHotspot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hotspot', models.CharField(blank=True, max_length=70, null=True)),
                ('count', models.IntegerField(blank=True, default=1, null=True)),
                ('variant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hotspots', to='api.variant')),
            ],
        ),

        migrations.RunPython(add_path_items),
    ]
