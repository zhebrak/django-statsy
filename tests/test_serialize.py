# coding: utf-8

from datetime import datetime

from django.test import TestCase

import statsy


class TestSerialization(TestCase):
    def setUp(self):
        self.statsy = statsy.Statsy(cache=False)

    def test_serialize_datetime(self):
        self.statsy.send(
            group='test',
            event='test_serialize'
        )
        self.instance = statsy.objects.first()

        try:
            self.instance.serialize()
        except Exception as e:
            self.fail('Serialization causes an error, {}'.format(e))

    def test_serialize_string(self):
        self.statsy.send(
            group='test',
            event='test_serialize'
        )
        self.instance = statsy.objects.first()
        self.instance.created_at = datetime.now().isoformat()

        try:
            str_serialization = self.instance.serialize()
            self.instance.refresh_from_db()
            self.assertEqual(self.instance.serialize(), str_serialization)
        except Exception as e:
            self.fail('Serialization causes an error, {}'.format(e))
