from django import template

register = template.Library()


@register.filter()
def filter_qs(q_set, key):
    """converts int to string"""
    q = q_set.filter(pk=key)[0]
    return q