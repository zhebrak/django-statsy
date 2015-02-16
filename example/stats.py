# coding: utf-8

from django.shortcuts import render_to_response
from django.views.generic import TemplateView

import statsy


class AverageLikeValuePerHour(TemplateView):
    template_name = 'example/stats.html'


def max_like_value_per_hour(request):
    return render_to_response('example/stats.html')


def min_like_value_per_hour(request):
    return render_to_response('example/stats.html')


statsy.site.register(max_like_value_per_hour, name='Max Like', category='Like')
statsy.site.register(min_like_value_per_hour, name='Min Like', category='Like')

statsy.site.register(
    AverageLikeValuePerHour.as_view(),
    category='Everyday',
    permission='stats.custom_permission'
)
