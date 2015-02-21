# coding: utf-8

from django.core.urlresolvers import reverse
from django.test import TestCase, Client

import statsy

from tests.settings import test_group, test_event, test_label, test_value_list


class ApiTest(TestCase):
    def setUp(self):
        self.statsy = statsy.Statsy(cache=False)
        self.client = Client()

    def test_send(self):
        for test_value in test_value_list:
            data = {
                'group': test_group, 'event': test_event,
                'label': test_label, 'value': test_value
            }

            if isinstance(test_value, (float, int)):
                data['value_type'] = 'number'

            self.client.post(
                reverse('statsy.send'),
                data=data
            )

            statsy_object = self.statsy.objects.select_related('group', 'event').order_by('pk').last()

            self.assertEqual(test_group, statsy_object.group.name)
            self.assertEqual(test_event, statsy_object.event.name)
            self.assertEqual(test_label, statsy_object.label)
            self.assertEqual(test_value, statsy_object.value)
