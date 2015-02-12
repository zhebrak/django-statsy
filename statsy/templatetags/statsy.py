# coding: utf-8

from django import template


register = template.Library()


@register.inclusion_tag('statsy/script.html')
def statsy():
    pass
