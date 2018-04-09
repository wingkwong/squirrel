from django import template

register = template.Library()

@register.filter
def get_by_index(lst, idx):
    return lst[idx-1]