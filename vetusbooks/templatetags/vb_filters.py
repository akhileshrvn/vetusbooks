from django import template

register = template.Library()

@register.filter(name='percent_four')
def percentFour(value):
    return value%4

@register.filter(name='list_length')
def percentFour(value):
    return len(value)