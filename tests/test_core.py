# coding: utf-8

import unittest

from statsy import statsy


class CoreTest(unittest.TestCase):
    def setUp(self):
        self.statsy = statsy

        self.group_name = 'test_group'
        self.event_name = 'test_event'
        self.label = 'test_label'
        self.value = 'test_value'

    def test_send_basic(self):
        self.statsy.send(group=self.group_name, event=self.event_name, label=self.label, value=self.value)

        statsy_object = self.statsy.objects.select_related('group', 'event').last()

        self.assertEqual(self.group_name, statsy_object.group.name)
        self.assertEqual(self.event_name, statsy_object.event.name)
        self.assertEqual(self.label, statsy_object.label)
        self.assertEqual(self.value, statsy_object.value)

