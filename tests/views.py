# coding: utf-8

from django.http import HttpResponse
from django.views.generic import View

import statsy

from statsy.mixins import WatchMixin
from tests.settings import test_group, test_event, test_value_list, test_label


class FunctionalViewFabric(object):
    @staticmethod
    def functional_view(request):
        return HttpResponse()

    def __iter__(self):
        for test_value in test_value_list:
            watch_params = {
                'group': test_group, 'event': test_event,
                'label': test_label, 'value': test_value
            }

            yield statsy.watch(**watch_params)(self.functional_view), watch_params


class CBVFabric(object):
    class CBVView(WatchMixin, View):
        watch_group = test_group
        watch_event = test_event
        watch_label = test_label

        def get(self, request):
            return HttpResponse()

    def __iter__(self):
        for test_value in test_value_list:
            class TestView(self.CBVView):
                watch_value = test_value

            yield TestView.as_view(), {
                'group': test_group, 'event': test_event,
                'label': test_label, 'value': test_value
            }


class ViewFabric(object):
    fabric_list = [FunctionalViewFabric, CBVFabric]

    def __iter__(self):
        for fabric in self.fabric_list:
            for view in fabric():
                yield view
