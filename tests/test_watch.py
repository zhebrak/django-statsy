# coding: utf-8

from django.core.urlresolvers import reverse
from django.test import Client, TestCase

from tests.urls import test_url_list

import statsy


class TestWatch(TestCase):
    def setUp(self):
        self.client = Client()

    def test_views(self):
        for url in test_url_list:
            response = self.client.get(reverse(url))
            self.assertEqual(response.status_code, 200)

        self.assertEqual(len(test_url_list), statsy.objects.count())
