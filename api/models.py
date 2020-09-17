from django.db import models
from django.contrib.auth.models import User

# Constant Pathogenic titles
ITEMS = {'PVS1': 10, 'PS1': 7, 'PS2': 7, 'PS3': 7, 'PS4': 7, 'PM': 2, 'PM1': 2, 'PM2': 2, 'PM3': 2, 'PM4': 2, 'PM5': 2, 'PM6': 2, 'PP1': 1, 'PP2': 1, 'PP3': 1, 'PP4': 1, 'PP5': 1,
		 'BA1': 16, 'BS1': 8, 'BS2': 8, 'BS3': 8, 'BS4': 8, 'BP1': 1, 'BP2': 1, 'BP3': 1, 'BP4': 1, 'BP5': 1, 'BP6': 1, 'BP7': 1}


# Create your models here.
class Gene(models.Model):
	name = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')
	content = models.TextField(blank=True)

	def __str__(self):
		return self.name

	def class_type(self):
		return "Gene"


class Variant(models.Model):
	genome_build = models.CharField(max_length=10, null=True)
	chromosome = models.CharField(max_length=6, null=True)
	start = models.CharField(max_length=10, null=True)
	end = models.CharField(max_length=10, null=True)
	ref = models.CharField(max_length=100, null=True)
	alt = models.CharField(max_length=100, null=True)
	transcript = models.CharField(max_length=20, null=True)
	c = models.CharField(max_length=10, null=True)
	p = models.CharField(max_length=20, null=True)
	consequence = models.CharField(max_length=10, null=True)
	gene = models.ForeignKey(Gene, related_name="variants", on_delete=models.CASCADE, null=True, blank=True)
	branch = models.CharField(choices=(
		('gp', "Genomic Pathogenetic"),
		('so', "Somatic Oncogenetic"),
	), max_length=2, default='gp')
	reported = models.CharField(choices=(
		('n', "Not checked"),
		('c', "Checked but not reported"),
		('r', "Reported"),
	), max_length=1, default='n')


class PathItem(models.Model):
	key = models.CharField(max_length=5, null=True)
	value = models.IntegerField(default=0)

	def __str__(self):
		return self.key


class Disease(models.Model):
	name = models.CharField(max_length=20, null=True)
	others = models.CharField(max_length=20, null=True)
	report = models.CharField(max_length=20, null=True)
	variant = models.ForeignKey(Variant, related_name="diseases", on_delete=models.CASCADE, null=True, blank=True)

	def __str__(self):
		return self.name


class Score(models.Model):
	for_score = models.CharField(max_length=20, null=True)
	against_score = models.CharField(max_length=20, null=True)
	disease = models.ForeignKey(Disease, related_name="score", on_delete=models.CASCADE, null=True, blank=True)


class Functional(models.Model):
	key = models.CharField(max_length=20, null=True)
	value = models.CharField(max_length=20, null=True)
	disease = models.ForeignKey(Disease, related_name="functionals", on_delete=models.CASCADE, null=True, blank=True)

	def __str__(self):
		return self.key


class Evidence(models.Model):
	TYPE_CHOICES = [
		('PM', 'PMID'),
		('O', 'Others'),
	]

	item = models.ForeignKey(PathItem, on_delete=models.CASCADE, null=True, blank=True)
	functional = models.ForeignKey(Functional, related_name="evidences", on_delete=models.CASCADE, null=True, blank=True)
	disease = models.ForeignKey(Disease, related_name="evidences", on_delete=models.CASCADE, null=True, blank=True)
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
	SIG_CHOICES = [
		('Pred', 'Predictive'),
		('Prog', 'Prognostic'),
		('Diag', 'Diagnostic'),
	]

	level = models.CharField(max_length=1, null=True)
	evid_sig = models.CharField(
		max_length=4,
		choices=SIG_CHOICES,
		default='Pred',
	)
	evid_dir = models.BooleanField(null=True)
	clin_sig = models.CharField(max_length=25)
	drug_class = models.TextField(null=True)
	evid_rating = models.IntegerField(default=1)
	evidence = models.ForeignKey(Evidence, related_name="subevidences", on_delete=models.CASCADE, null=True, blank=True)
	variant = models.ForeignKey(Variant, related_name="subevidences", on_delete=models.CASCADE, null=True, blank=True)

	def __str__(self):
		return self.clin_sig


class Report(models.Model):
	name = models.CharField(max_length=40)
	content = models.TextField(null=True)
	disease = models.ForeignKey(Disease, related_name="reports", on_delete=models.CASCADE, null=True, blank=True)

	def __str__(self):
		return self.content


class History(models.Model):
	content = models.TextField(null=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	object = models.ForeignKey(Evidence, verbose_name='field', related_name="histories", on_delete=models.CASCADE, null=True, blank=True)
	variant = models.ForeignKey(Variant, related_name="history", on_delete=models.CASCADE, null=True, blank=True)

	class Meta:
		ordering = ['timestamp']

	def __str__(self):
		return str(self.user) + " / " + self.timestamp.strftime('%Y-%m-%d')


class Interpretation(models.Model):
	content = models.TextField(blank=True)
	genes = models.ManyToManyField(Gene, related_name='interpretations')
	variants = models.ManyToManyField(Variant, related_name='interpretations')
