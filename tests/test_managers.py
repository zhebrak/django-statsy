# coding: utf-8

from django.test import TestCase

import statsy

from tests.settings import test_group, test_event, test_label


class ManagersTest(TestCase):
    def setUp(self):
        self.statsy = statsy.Statsy(cache=False)
        self.test_count = 10

    def test_by_group(self):
        for idx, group in enumerate([test_group] * self.test_count):
            self.statsy.send(
                group='{0}_{1}'.format(group, str(idx % 2)),
            )

        for idx in [0, 1]:
            group_name = '{0}_{1}'.format(test_group, idx)
            stats_list = self.statsy.objects.by_group(group_name)

            self.assertEqual(
                stats_list.count(), self.test_count / 2
            )

            for stats in stats_list:
                self.assertEqual(stats.group.name, group_name)

    def test_by_event(self):
        for idx, event in enumerate([test_event] * self.test_count):
            self.statsy.send(
                event='{0}_{1}'.format(event, str(idx % 2)),
            )

        for idx in [0, 1]:
            event_name = '{0}_{1}'.format(test_event, idx)
            stats_list = self.statsy.objects.by_event(event_name)

            self.assertEqual(
                stats_list.count(), self.test_count / 2
            )

            for stats in stats_list:
                self.assertEqual(stats.event.name, event_name)

    def test_by_label(self):
        for idx, label in enumerate([test_label] * self.test_count):
            self.statsy.send(
                label='{0}_{1}'.format(label, str(idx % 2)),
            )

        for idx in [0, 1]:
            label_name = '{0}_{1}'.format(test_label, idx)
            stats_list = self.statsy.objects.by_label(label_name)

            self.assertEqual(
                stats_list.count(), self.test_count / 2
            )

            for stats in stats_list:
                self.assertEqual(stats.label, label_name)
