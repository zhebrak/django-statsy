# coding: utf-8

from django.test import TestCase

import statsy


class LogTest(TestCase):
    def test_log(self):
        statsy.logger.info('TEST info message')
        statsy.logger.error('TEST error message')
