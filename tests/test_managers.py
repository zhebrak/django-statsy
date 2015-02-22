# coding: utf-8

from django.contrib.auth import get_user_model
from django.test import TestCase

import statsy

from statsy.models import StatsyGroup

from tests.settings import test_group, test_event, test_label, test_username, test_password, test_value_list


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

    def test_by_user(self):
        for idx in [0, 1]:
            user = get_user_model().objects.create_user(
                '{0}_{1}'.format(test_username, idx), 'test@test.com', test_password
            )

            for _ in range(self.test_count):
                self.statsy.send(user=user)

        for idx in [0, 1]:
            username = '{0}_{1}'.format(test_username, idx)
            user = get_user_model().objects.get(username=username)

            stats_list_str = self.statsy.objects.by_user(username)
            stats_list_id = self.statsy.objects.by_user(user.id)
            stats_list_obj = self.statsy.objects.by_user(user)

            for stats_list in [stats_list_str, stats_list_id, stats_list_obj]:
                self.assertEqual(stats_list.count(), self.test_count)

                for stats in stats_list:
                    self.assertEqual(stats.user.username, username)

    def test_active(self):
        for idx, test_value in enumerate(test_value_list):
            self.statsy.send(
                group=test_group, event=test_event,
                label=test_label, value=test_value
            )

        group = StatsyGroup.objects.get(name=test_group)

        group.activate()
        self.assertEqual(self.statsy.objects.active().count(), len(test_value_list))
        self.assertEqual(self.statsy.groups.active().count(), 1)

        group.deactivate()
        self.assertEqual(self.statsy.objects.active().count(), 0)
        self.assertEqual(self.statsy.groups.active().count(), 0)
