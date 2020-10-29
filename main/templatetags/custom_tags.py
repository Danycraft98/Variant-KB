from django import template
from api.models import Disease

register = template.Library()


@register.filter(name='get_class')
def get_class(value):
	return value.__class__.__name__


@register.filter(name='get_disease')
def get_disease(name):
	return [disease.name for disease in Disease.objects.filter(name=name)]
