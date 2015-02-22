# coding: utf-8

from django.test import TestCase, override_settings

import statsy

from tests.settings import test_group, test_event, test_label, test_value_list


class CoreTest(TestCase):
    def setUp(self):
        self.statsy = statsy.Statsy(cache=False)

    def test_send_basic(self):
        for test_value in test_value_list:
            self.statsy.send(
                group=test_group, event=test_event,
                label=test_label, value=test_value
            )

            statsy_object = self.statsy.objects.select_related('group', 'event').order_by('pk').last()

            self.assertEqual(test_group, statsy_object.group.name)
            self.assertEqual(test_event, statsy_object.event.name)
            self.assertEqual(test_label, statsy_object.label)
            self.assertEqual(test_value, statsy_object.value)

    @override_settings(STATSY_ASYNC=True)
    def test_send_async(self):
        # It falls back to ASYNC=False mode
        from statsy.tasks import send

        statsy_async = statsy.Statsy(async=True)

        for test_value in test_value_list:
            statsy_async.send(
                group=test_group, event=test_event,
                label=test_label, value=test_value
            )
