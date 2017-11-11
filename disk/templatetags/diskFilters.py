from django import template

register = template.Library()

@register.filter(name='cutPrefix')
def cutPrefix(value, arg):
    return value.replace(arg, '', 1)

@register.filter(name='fileSize')
def fileSize(value):
    value=int(value)
    if value>=1000000000:
        return "%.1f G" % (value/1000000000)
    if value>=1000000:
        return "%.1f M" % (value/1000000)
    if value>=1000:
        return "%.1f K" % (value/1000)
    else:
        return "%d B" % value
