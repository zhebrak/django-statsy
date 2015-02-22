# coding: utf-8

from django.test import TestCase

import statsy


class LogTest(TestCase):
    def test_log(self):
        statsy.logger.info('INFO message')
        statsy.logger.error('Error message')
