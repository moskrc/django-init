# -*- coding: utf-8
from django.utils.safestring import mark_safe
from django.utils.encoding import smart_unicode
import decimal
from django import template
from django.template.defaultfilters import stringfilter
import re
import itertools
import copy

def textbreaker(text,breaker='<!-- break -->',more_symbols='...'):
    try:
        pos = text.index(breaker)
    except:
        return mark_safe(text)
    
    return mark_safe(text[:pos].rstrip())+more_symbols


