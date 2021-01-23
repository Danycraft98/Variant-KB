from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory

from api.constants import *
from api.models import *

__all__ = [
    'SODiseaseFormSet', 'GPDiseaseFormSet', 'EvidenceFormSet', 'PathItemFormSet'
]


# Base Forms------------------------------------------------------------------------------------------------------
class DiseaseForm(forms.ModelForm):
    id = forms.CharField(required=False, widget=forms.HiddenInput())
    child_id = forms.CharField(required=False, widget=forms.HiddenInput())
    branch = forms.ChoiceField(initial='so', choices=[('no', 'No Disease')] + BRANCH_CHOICES, widget=forms.RadioSelect(attrs={
        'class': 'form-check-inline',
        'onchange': 'change_disease(this)'
    }))
    name = forms.CharField(required=False, label='Disease Name', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'list': 'datalistOptions',
        'placeholder': 'Enter Name...',
        'oninput': 'get_report(this);updateHeader(this)'
    }))
    report = forms.CharField(required=False, label='Germline Clinical Report', widget=forms.Textarea(attrs={
        'class': 'form-control',
        'rows': '2'
    }))
    others = forms.ChoiceField(required=False, label='Tier', choices=TIER_CHOICES, widget=forms.Select(attrs={
        'class': 'form-select',
    }))

    class Meta:
        model = Disease
        fields = ['id', 'branch', 'name', 'report', 'others']  # 'reviewed', ]

    def _clean_fields(self):
        for name, field in self.fields.items():
            if field.disabled:
                value = self.get_initial_for_field(field, name)
            else:
                value = field.widget.value_from_datadict(self.data, self.files, self.add_prefix(name))

            try:
                if isinstance(field, forms.FileField):
                    initial = self.get_initial_for_field(field, name)
                    value = field.clean(value, initial)
                else:
                    value = field.clean(value)

                self.cleaned_data[name] = value
                #if name == 'id' and Disease.objects.filter(id=self.cleaned_data['id']).exists():
                #    raise ValidationError('Disease already exists')

                if hasattr(self, 'clean_%s' % name):
                    value = getattr(self, 'clean_%s' % name)()
                    self.cleaned_data[name] = value

            except ValidationError as e:
                self.add_error(name, e)

    def clean(self):
        super(DiseaseForm, self).clean()
        return self.cleaned_data


class EvidenceForm(forms.ModelForm):
    key = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input',
        'onclick': 'select_evidence(this)'
    }))
    id = forms.CharField(required=False, widget=forms.HiddenInput())
    source_type = forms.ChoiceField(required=False, choices=TYPE_CHOICES, widget=forms.Select(attrs={
        'class': 'form-select'
    }))
    source_id = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Source ID'
    }))
    statement = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'rows': '2'
    }))

    evid_sig = forms.ChoiceField(required=False, choices=EVID_SIG_CHOICES, widget=forms.Select(attrs={
        'class': 'form-select'
    }))
    level = forms.ChoiceField(required=False, choices=EVID_LEVEL_CHOICES, widget=forms.Select(attrs={
        'class': 'form-select'
    }))
    evid_dir = forms.ChoiceField(required=False, choices=EVID_DIR_CHOICES, widget=forms.Select(attrs={
        'class': 'form-select'
    }))
    clin_sig = forms.ChoiceField(required=False, choices=CLIN_SIG_CHOICES, widget=forms.Select(attrs={
        'class': 'form-select'
    }))
    drug_class = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': ''
    }))
    evid_rating = forms.ChoiceField(required=False, choices=EVID_RATING_CHOICES, widget=forms.Select(attrs={
        'class': 'form-select'
    }))
    prefix = 'evid_'

    class Meta:
        model = Evidence
        fields = '__all__'

    def _clean_fields(self):
        for name, field in self.fields.items():
            if field.disabled:
                value = self.get_initial_for_field(field, name)
            else:
                value = field.widget.value_from_datadict(self.data, self.files, self.add_prefix(name))

            try:
                if isinstance(field, forms.FileField):
                    initial = self.get_initial_for_field(field, name)
                    value = field.clean(value, initial)
                else:
                    value = field.clean(value)

                self.cleaned_data[name] = value
                if name == 'id' and Evidence.objects.filter(id=self.cleaned_data['id']).exists():
                    raise ValidationError('Evidence already exists')

                if hasattr(self, 'clean_%s' % name):
                    value = getattr(self, 'clean_%s' % name)()
                    self.cleaned_data[name] = value

            except ValidationError as e:
                self.add_error(name, e)

    def clean(self):
        super(EvidenceForm, self).clean()
        return self.cleaned_data


EvidenceFormSet = inlineformset_factory(
    Evidence,
    SubEvidence,
    form=EvidenceForm,
    min_num=1,
    extra=1
)


# Somatic Oncogenicity ------------------------------------------------------------------------------------------
class SODiseaseForm(DiseaseForm):
    key = forms.ChoiceField(required=False, label='Functional Significance', choices=FUNC_SIG_CHOICES, widget=forms.Select(attrs={
        'class': 'form-select',
    }))
    value = forms.ChoiceField(required=False, label='Functional Category', choices=FUNC_CAT_CHOICES, widget=forms.Select(attrs={
        'class': 'form-select',
    }))
    prefix = 'so_'

    class Meta:
        model = Functional
        fields = '__all__'

    def clean(self):
        super(SODiseaseForm, self).clean()
        return self.cleaned_data


SODiseaseFormSet = inlineformset_factory(
    Disease,
    Functional,
    form=SODiseaseForm,
    min_num=1,
)


# Germline Pathogenicity------------------------------------------------------------------------------------------
class GPDiseaseForm(DiseaseForm):
    branch = forms.ChoiceField(initial='gp', choices=[('no', 'No Disease')] + BRANCH_CHOICES, widget=forms.RadioSelect(attrs={
        'class': 'form-check-inline',
        'onchange': 'change_disease(this)'
    }))

    for_score = forms.CharField(required=False, label='For Pathogenicity', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'readonly': ''
    }))
    against_score = forms.CharField(required=False, label='Against Pathogenicity', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'readonly': ''
    }))
    content = forms.CharField(required=False, label='ACMG Classification', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'readonly': ''
    }))
    prefix = 'gp_'


class PathItemForm(forms.ModelForm):
    key = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input',
        'value': 'False'
    }))
    content = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    prefix = 'item_'

    class Meta:
        model = PathItem
        fields = '__all__'

    def clean(self):
        super(PathItemForm, self).clean()
        return self.cleaned_data


PathItemFormSet = inlineformset_factory(
    PathItem, Evidence,
    form=PathItemForm,
    fields='__all__',
    extra=29
)
GPDiseaseFormSet = inlineformset_factory(
    Disease,
    Score,
    form=GPDiseaseForm,
    min_num=1,
)
