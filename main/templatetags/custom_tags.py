from django import template

register = template.Library()


@register.filter
def url_links(value, arg):
    return ";".join(["<a href='http://pubmed.ncbi.nlm.nih.gov/" + pmid + "' target='_blank'>" + pmid + '</a>' for pmid in value.split(arg)])


@register.filter
def zip_list(list1, list2):
    return zip(list1, list2)


@register.filter
def get_index(formset, index):
    return formset[index] if len(formset) > index else None


@register.filter
def is_empty_form(form):
    return 'prefix' in form.prefix


@register.filter
def data_verbose(input_field):
    data = input_field.data
    field = input_field.field
    return hasattr(field, 'choices') and dict(field.choices).get(data,'') or data
