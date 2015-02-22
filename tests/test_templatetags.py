# coding: utf-8

from django.template import Template, Context
from django.test import TestCase


class TemplateTagTest(TestCase):
    def test_templatetag_statsy(self):
        template = Template('{% load statsy %} {% statsy %}')
        rendered = template.render(Context())

        self.assertIn('/statsy/api.js"></script>', rendered)
        self.assertIn('<input type="hidden" id="statsy_send_url"', rendered)
