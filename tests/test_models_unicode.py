# coding: utf-8

from django.test import TestCase

import statsy

from tests.settings import test_group, test_event, test_label, test_value_list


class ModelsUnicodeTest(TestCase):
    def setUp(self):
        self.statsy = statsy.Statsy(cache=False)

        for test_value in test_value_list:
            self.statsy.send(
                group=test_group, event=test_event,
                label=test_label, value=test_value
            )

    def test_models_unicode(self):
        for stats in self.statsy.objects.all():
            self.assertIsInstance(str(stats), str)
            self.assertIsInstance(str(stats.group), str)
            self.assertIsInstance(str(stats.event), str)
