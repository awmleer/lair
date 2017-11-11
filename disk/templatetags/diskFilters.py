from django import template

register = template.Library()

@register.filter(name='cutPrefix')
def cutPrefix(value, arg):
    return value.replace(arg, '', 1)

