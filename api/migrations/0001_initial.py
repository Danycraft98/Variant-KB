# Generated by Django 3.1 on 2020-11-12 21:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


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
                ('name', models.CharField(max_length=20, null=True)),
                ('others', models.CharField(max_length=20, null=True)),
                ('report', models.CharField(max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Evidence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_type', models.CharField(choices=[('PM', 'PMID'), ('O', 'Others')], default='PM', max_length=2)),
                ('source_id', models.CharField(max_length=20, null=True)),
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
                ('content', models.TextField(blank=True)),
                ('germline_content', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='PathItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=5, null=True)),
                ('value', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Variant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genome_build', models.CharField(max_length=10, null=True, verbose_name='genome build')),
                ('chr', models.CharField(max_length=6, null=True, verbose_name='Chromosome')),
                ('start', models.CharField(max_length=10, null=True)),
                ('end', models.CharField(max_length=10, null=True)),
                ('ref', models.CharField(max_length=100, null=True)),
                ('alt', models.CharField(max_length=100, null=True)),
                ('transcript', models.CharField(max_length=20)),
                ('cdna', models.CharField(max_length=10, null=True, verbose_name='c.')),
                ('protein', models.CharField(max_length=20, verbose_name='p.')),
                ('consequence', models.CharField(max_length=10, null=True)),
                ('exonic_function', models.CharField(max_length=20, null=True)),
                ('content', models.TextField(blank=True)),
                ('germline_content', models.TextField(blank=True)),
                ('af', models.CharField(max_length=20, null=True, verbose_name='AF')),
                ('af_popmax', models.CharField(max_length=20, null=True, verbose_name='AF_popmax')),
                ('cosmic70', models.CharField(max_length=20, null=True)),
                ('clinvar', models.CharField(max_length=20, null=True, verbose_name='CLINVAR')),
                ('insilicodamaging', models.CharField(max_length=20, null=True, verbose_name='InSilicoDamaging')),
                ('insilicobenign', models.CharField(max_length=100, null=True, verbose_name='InSilicoBenign')),
                ('polyphen2_hdiv_pred', models.CharField(max_length=4, null=True, verbose_name='Polyphen2_HDIV_pred')),
                ('polyphen2_hvar_pred', models.CharField(max_length=4, null=True, verbose_name='Polyphen2_HVAR_pred')),
                ('sift_pred', models.CharField(max_length=4, null=True, verbose_name='SIFT_pred')),
                ('mutationtaster_pred', models.CharField(max_length=4, null=True, verbose_name='MutationTaster_pred')),
                ('mutationassessor_pred', models.CharField(max_length=4, null=True, verbose_name='MutationAssessor_pred')),
                ('provean_pred', models.CharField(max_length=4, null=True, verbose_name='PROVEAN_pred')),
                ('lrt_pred', models.CharField(max_length=4, null=True, verbose_name='LRT_pred')),
                ('tcga', models.CharField(max_length=20, null=True, verbose_name='TCGA#occurances')),
                ('oncokb', models.CharField(max_length=500, null=True, verbose_name='oncoKB')),
                ('oncokb_pmids', models.CharField(max_length=50, null=True, verbose_name='oncoKB_PMIDs')),
                ('watson', models.CharField(max_length=20, null=True)),
                ('watson_pmids', models.CharField(max_length=50, null=True, verbose_name='Watson_PMIDs')),
                ('qci', models.CharField(max_length=20, null=True, verbose_name='QCI')),
                ('qci_pmids', models.CharField(max_length=50, null=True, verbose_name='QCI_PMIDs')),
                ('pmkb', models.CharField(max_length=10, null=True, verbose_name='PMKB')),
                ('pmkb_citations', models.CharField(max_length=500, null=True, verbose_name='PMKB_citations')),
                ('civic', models.CharField(max_length=50, null=True, verbose_name='CIViC')),
                ('google', models.CharField(max_length=100, null=True)),
                ('alamut', models.CharField(max_length=70, null=True)),
                ('reviewed', models.CharField(choices=[('n', 'not reviewed'), ('r', 'reviewed'), ('m', "meta-reviewed"), ('a', 'approved')], default='n', max_length=1)),
                ('reviewed_date', models.DateTimeField(null=True, verbose_name='reviewed date')),
                ('review_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviewed_variants', to=settings.AUTH_USER_MODEL)),
                ('meta_reviewed_date', models.DateTimeField(null=True, verbose_name='meta-reviewed date')),
                ('meta_review_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='meta_reviewed_variants', to=settings.AUTH_USER_MODEL)),
                ('approved_date', models.DateTimeField(null=True, verbose_name='approved date')),
                ('approve_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='approved_variants', to=settings.AUTH_USER_MODEL)),
                ('gene', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='variants', to='api.gene')),
            ],
        ),
        migrations.CreateModel(
            name='SubEvidence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(max_length=1, null=True)),
                ('evid_sig', models.CharField(choices=[('Pred', 'Predictive'), ('Prog', 'Prognostic'), ('Diag', 'Diagnostic')], default='Pred', max_length=4)),
                ('evid_dir', models.BooleanField(null=True)),
                ('clin_sig', models.CharField(max_length=25)),
                ('drug_class', models.TextField(null=True)),
                ('evid_rating', models.IntegerField(default=1)),
                ('evidence', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subevidences', to='api.evidence')),
                ('variant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subevidences', to='api.variant')),
            ],
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('for_score', models.CharField(max_length=20, null=True)),
                ('against_score', models.CharField(max_length=20, null=True)),
                ('disease', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='score', to='api.disease')),
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
            name='Interpretation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True)),
                ('genes', models.ManyToManyField(related_name='interpretations', to='api.Gene')),
                ('variants', models.ManyToManyField(related_name='interpretations', to='api.Variant')),
            ],
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(null=True)),
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
                ('key', models.CharField(max_length=20, null=True)),
                ('value', models.CharField(max_length=20, null=True)),
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
                ('hotspot', models.CharField(max_length=70, null=True)),
                ('count', models.IntegerField(default=1)),
                ('variant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hotspots', to='api.variant')),
            ],
        ),
    ]
