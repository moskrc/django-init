# -*- coding: utf-8
from django.forms import CheckboxInput
from django import template


register = template.Library()


@register.filter
def is_checkbox(item):
    return isinstance(item.field.widget, CheckboxInput)


@register.filter
def htmlattributes(value, arg):
    attrs = value.field.widget.attrs
    data = arg
    kvs = data.split(',')

    for string in kvs:
        kv = string.split(':')
        attrs[kv[0]] = kv[1]

    rendered = str(value)

    return rendered

