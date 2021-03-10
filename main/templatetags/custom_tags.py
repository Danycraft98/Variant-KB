from django import template

from api.constants import TYPE_CHOICES

register = template.Library()


@register.filter
def get_fields(arg_dict, evid_type=None):
    labels = {'Id': 'id', 'Source type': 'source_type', 'Source id': 'source_id', 'Statement': 'statement'}
    return_list = [{'label': key} for key in labels]
    [item.update({'value': arg.__dict__.get(label, '')})
     for item, label in zip(return_list, labels.values()) for arg in arg_dict
     if hasattr(arg, label) and ((evid_type == 'func' and arg.functional) or (not evid_type and not arg.functional and not arg.item))
     ]
    [item.update({'value': arg.__dict__.get(label, ''), 'item': arg.item.key})
     for item, label in zip(return_list, labels.values()) for arg in arg_dict
     if hasattr(arg, label) and (evid_type == 'item' and arg.item)
     ]
    return_list[1]['cust_choices'] = TYPE_CHOICES
    return return_list


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
def equals(arg1, arg2):
    return arg1 == arg2


@register.filter
def data_verbose(input_field, attr):
    value = input_field.value()
    field = input_field.field
    if not isinstance(attr, str):
        return all(dx.name not in value for dx in attr)
    return hasattr(field, attr) and dict(field.choices).get(value, '') or value


@register.filter
def evidence_exist(evids, pathitem):
    return any(pathitem == e.item.key for e in evids)


@register.filter
def get_act_dx(diseases):
    return diseases.filter(functional=None, item=None)
