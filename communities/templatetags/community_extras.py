from django import template

register = template.Library()

@register.filter
def split(value, arg):
    """Split the value by the argument and return the last part"""
    return value.split(arg)[-1] 