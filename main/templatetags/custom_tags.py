from django import template

register = template.Library()


@register.filter(name='url_links')
def split(value, arg):
    return ";".join(["<a href='http://pubmed.ncbi.nlm.nih.gov/" + pmid + "' target='_blank'>" + pmid + '</a>' for pmid in value.split(arg)])
