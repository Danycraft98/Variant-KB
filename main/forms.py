from django import forms
from nested_formset import (
    nestedformset_factory, BaseNestedModelForm, inlineformset_factory, BaseInlineFormSet
)

from api.models import *
from api.constants import *

__all__ = ['GPDiseaseFormSet', 'SODiseaseFormSet']

# Germline ------------------------------------------------------------------------------------------


class GPDiseaseBaseForm(BaseNestedModelForm):
    id = forms.CharField(required=False, widget=forms.HiddenInput())
    branch = forms.ChoiceField(initial='gp', choices=BRANCH_CHOICES, widget=forms.RadioSelect(attrs={
        'class': 'form-inline'
    }))
    name = forms.CharField(label='Disease Name', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'list': 'datalistOptions',
        'placeholder': 'Enter Name...',
        'oninput': 'get_report(this);update_header(this)'
    }))
    report = forms.CharField(label='Germline Clinical Report', widget=forms.Textarea(attrs={
        'class': 'form-control',
        'rows': '2'
    }))
    others = forms.ChoiceField(label='Tier', choices=TIER_CHOICES, required=False, widget=forms.Select(attrs={
        'class': 'form-control',
    }))

    class Meta:
        model = Disease
        fields = ['id', 'branch', 'name', 'report', 'others']  # 'reviewed', ]


class ScoreForm(forms.ModelForm):
    id = forms.CharField(required=False, widget=forms.HiddenInput())
    for_score = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'readonly': ''
    }))
    against_score = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'readonly': ''

    }))
    content = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'readonly': ''
    }))

    class Meta:
        model = Score
        fields = '__all__'


class EvidenceForm(forms.ModelForm):
    key = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input',
        'onclick': 'select_evidence(this)'
    }))
    id = forms.CharField(required=False, widget=forms.HiddenInput())
    source_type = forms.ChoiceField(required=False, choices=TYPE_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control'
    }))
    source_id = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Source ID'
    }))
    statement = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'rows': '2'
    }))

    class Meta:
        model = Evidence
        fields = '__all__'


GPDiseaseFormSet = inlineformset_factory(
    Disease,
    Evidence,
    extra=1,
    form=GPDiseaseBaseForm,
)
# Somatic ------------------------------------------------------------------------------------------


class SODiseaseBaseForm(BaseNestedModelForm):
    id = forms.CharField(required=False, widget=forms.HiddenInput())
    branch = forms.ChoiceField(initial='so', choices=BRANCH_CHOICES, widget=forms.RadioSelect(attrs={
        'class': 'form-inline'
    }))
    name = forms.CharField(label='Disease Name', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'list': 'datalistOptions',
        'placeholder': 'Enter Name...',
        'oninput': 'get_report(this);update_header(this)'
    }))
    report = forms.CharField(label='Germline Clinical Report', widget=forms.Textarea(attrs={
        'class': 'form-control',
        'rows': '2'
    }))
    others = forms.ChoiceField(label='Tier', choices=TIER_CHOICES, required=False, widget=forms.Select(attrs={
        'class': 'form-control',
    }))

    class Meta:
        model = Disease
        fields = ['id', 'branch', 'name', 'report', 'others']  # 'reviewed', ]


class FunctionalBaseFormSet(BaseInlineFormSet):
    id = forms.CharField(required=False, widget=forms.HiddenInput())
    key = forms.ChoiceField(label='Functional Significance', choices=FUNC_SIG_CHOICES, required=False, widget=forms.Select(attrs={
        'class': 'form-control',
    }))
    value = forms.ChoiceField(label='Functional Category', choices=FUNC_CAT_CHOICES, required=False, widget=forms.Select(attrs={
        'class': 'form-control',
    }))

    class Meta:
        model = Functional
        fields = '__all__'


class SubEvidenceFormSet(BaseInlineFormSet):
    id = forms.CharField(required=False, widget=forms.HiddenInput())
    evid_sig = forms.ChoiceField(required=False, choices=EVID_SIG_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control',
        'onchange': "selectChange(this, '_clin_sig')"
    }))
    level = forms.ChoiceField(required=False, choices=EVID_LEVEL_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control',
        'onchange': "tierChange(this, ['A', 'B'], 'Tier I')"
    }))
    evid_dir = forms.ChoiceField(required=False, choices=EVID_DIR_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control'
    }))
    clin_sig = forms.ChoiceField(required=False, choices=CLIN_SIG_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control'
    }))
    drug_class = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    evid_rating = forms.ChoiceField(required=False, choices=CLIN_SIG_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = SubEvidence
        fields = '__all__'


SODiseaseFormSet = nestedformset_factory(
    Disease,
    Functional,
    form=SODiseaseBaseForm,
    extra=1,
    #formset=FunctionalBaseFormSet,
    nested_formset=inlineformset_factory(
        Evidence, SubEvidence, form=EvidenceForm,
        formset=SubEvidenceFormSet,
        extra=1, fields='__all__'
    ),
)
