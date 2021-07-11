from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def limit_len(value, limit):
    return value if len(value) <= limit else value[:limit+1] + '...'