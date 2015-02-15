# coding: utf-8

from django.shortcuts import render_to_response
from django.views.generic import TemplateView

import statsy


class AverageLikeValuePerHour(TemplateView):
    template_name = 'example/stats2.html'


def average_like_value_per_hour(request):
    return render_to_response('example/stats.html')


statsy.site.register(average_like_value_per_hour)
statsy.site.register(AverageLikeValuePerHour.as_view(), category='Everyday')
