# coding: utf-8

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase, Client

import statsy


class DashboardTest(TestCase):
    def setUp(self):
        self.statsy = statsy.Statsy(cache=False)
        self.client = Client()

        test_username = 'test'
        test_password = 'test'

        get_user_model().objects.create_superuser(test_username, 'test@test.com', test_password)

        self.client.login(
            username=test_username,
            password=test_password
        )

    def test_dashboard(self):
        response = self.client.get(reverse('statsy.dashboard'))

        self.assertEqual(response.status_code, 200)
