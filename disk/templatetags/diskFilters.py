from django import template
from django.utils import timezone

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

@register.filter(name='timeStampToString')
def timeStampToString(value):
    print(timezone.get_current_timezone())
    t=timezone.datetime.fromtimestamp(int(value)/10000000,tz=timezone.get_current_timezone())
    # t=timezone.localtime(t)
    return t.strftime("%Y-%m-%d %H:%M:%S")
