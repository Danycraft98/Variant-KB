from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory, modelformset_factory

from api.constants import REVIEWED_CHOICES, FUNC_SIG_CHOICES
from api.models import *

__all__ = [
    'DiseaseFormSet', 'ScoreFormSet', 'FunctionalFormSet',
    'PathItemFormSet', 'ReportFormSet'
]


# Base Forms------------------------------------------------------------------------------------------------------
class BaseForm(forms.ModelForm):

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
                if hasattr(self, 'clean_%s' % name):
                    value = getattr(self, 'clean_%s' % name)()
                    self.cleaned_data[name] = value

            except ValidationError as e:
                self.add_error(name, e)

    def clean(self):
        super(BaseForm, self).clean()
        return self.cleaned_data


class DiseaseForm(BaseForm):
    prefix = 'dx'
    reviewed = forms.MultipleChoiceField(label='Reviewed Status', initial='n', choices=REVIEWED_CHOICES, widget=forms.CheckboxSelectMultiple(
        attrs={'class': 'form-check-inline'}
    ))

    class Meta:
        model = Disease
        fields = '__all__'
        exclude = ['variant']

    def clean(self):
        clean_data = self.cleaned_data
        if clean_data.get('reviewed'):
            clean_data['reviewed'] = clean_data.get('reviewed')[-1]

        if clean_data.get('name', '') != '' and clean_data.get('branch', 'no') != 'no':
            super(DiseaseForm, self).clean()
        return clean_data


class ReportForm(BaseForm):
    prefix = 'report'
    id = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = Report
        fields = '__all__'
        exclude = ['DELETE', 'evidence', 'key']

    def clean(self):
        super(ReportForm, self).clean()
        return self.cleaned_data


class DiseaseFormSet(modelformset_factory(
    Disease,
    form=DiseaseForm,
    fields='__all__',
    min_num=0,
    extra=10
)):

    def get_queryset(self):
        return super(DiseaseFormSet, self).get_queryset().order_by('branch')


ReportFormSet = modelformset_factory(
    Report,
    form=ReportForm,
    fields='__all__',
    min_num=1,
    extra=6,
)


# Somatic Oncogenicity ------------------------------------------------------------------------------------------
class FunctionalForm(BaseForm):
    prefix = 'func'
    id = forms.CharField(required=False, widget=forms.HiddenInput())
    value = forms.ChoiceField(choices=FUNC_SIG_CHOICES, widget=forms.Select(attrs={
        'class': 'form-select',
        'onchange': "tierChange(this, ['Benign', 'None'], 'Tier IV')"
    }))

    class Meta:
        model = Functional
        fields = '__all__'

    def clean(self):
        super(FunctionalForm, self).clean()
        return self.cleaned_data


FunctionalFormSet = inlineformset_factory(
    Disease,
    Functional,
    form=FunctionalForm,
    min_num=1,
    extra=1
)


# Germline Pathogenicity------------------------------------------------------------------------------------------
class ScoreForm(BaseForm):
    prefix = 'score'
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

    class Meta:
        model = Score
        fields = '__all__'


class PathItemForm(BaseForm):
    prefix = 'item'
    key = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input',
        'value': 'False'
    }))
    value = forms.CharField(required=False, widget=forms.HiddenInput())
    content = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))

    class Meta:
        model = PathItem
        fields = '__all__'

    def clean(self):
        super(PathItemForm, self).clean()
        return self.cleaned_data


ScoreFormSet = inlineformset_factory(
    Disease,
    Score,
    form=ScoreForm,
    min_num=1,
)
PathItemFormSet = modelformset_factory(
    PathItem,
    form=PathItemForm,
    fields='__all__',
    min_num=29
)
