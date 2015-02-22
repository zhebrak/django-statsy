# coding: utf-8

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase, Client

import statsy

from tests.settings import test_username, test_password, test_group, test_event, test_label, test_value_list


class DashboardTest(TestCase):
    def setUp(self):
        self.statsy = statsy.Statsy(cache=False)
        self.client = Client()

        get_user_model().objects.create_superuser(test_username, 'test@test.com', test_password)

        self.client.login(
            username=test_username,
            password=test_password
        )

        for test_value in test_value_list:
            statsy.send(
                group=test_group, event=test_event,
                label=test_label, value=test_value
            )

    def test_dashboard(self):
        response = self.client.get(reverse('statsy.dashboard'))

        self.assertEqual(response.status_code, 200)

    def test_custom(self):
        response = self.client.get(reverse('statsy.custom'))

        self.assertEqual(response.status_code, 200)

    def test_today_group_stats(self):
        response = self.client.get(reverse('statsy.today_group_stats'))

        self.assertEqual(response.status_code, 200)

    def test_today_event_stats(self):
        response = self.client.get(reverse('statsy.today_event_stats'))

        self.assertEqual(response.status_code, 200)
