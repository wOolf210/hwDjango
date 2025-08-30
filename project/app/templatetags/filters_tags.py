
from django import template
from django.template.defaultfilters import stringfilter


register=template.Library()

@register.filter(name="currency")
def currency(value,iso="KZT"):
    try:
        value = float(value)
    except (TypeError,ValueError):
        return value
    return f"{value:,.2f}\u00A0{iso}"

@register.filter(is_safe=True) #> < <b>hello</b>
@stringfilter
def reverse_str(value):
    return value[::-1]

@register.simple_tag
def join_with(operator,*items):
    return operator.join(items)

from django.utils import timezone
@register.simple_tag(takes_context=True)
def show_time(context,fmt="%d.%m.%Y %H:%M:%S"):
    tz=timezone.get_current_timezone()
    return timezone.localtime(timezone.now(),tz).strftime(fmt)

@register.inclusion_tag("bullet.html")
def bullet(*items):
    return {"items":items,"count":len(items)}

@register.filter
def slice_v2(value):
    value=str(value)
    length=int(len(value)/2)
    return value[:length]

@register.filter
def change_digit(value):
    value=str(value)
    result=[]
    for i in value:
        if i.isdigit():
            result.append("*")
        else:
            result.append(i)
    return "".join(result)