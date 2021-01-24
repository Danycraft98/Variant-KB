from django import template

register = template.Library()


@register.filter
def url_links(value, arg):
    return ";".join(["<a href='http://pubmed.ncbi.nlm.nih.gov/" + pmid + "' target='_blank'>" + pmid + '</a>' for pmid in value.split(arg)])


@register.filter
def zip_list(list1, list2):
    return zip(list1, list2)
