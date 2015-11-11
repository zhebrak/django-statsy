# coding: utf-8

from statsy.helpers import get_correct_value_field


class ValueDescriptor(object):
    def get_field_name(self, value_type):
        return '_'.join([value_type, 'value'])

    def __init__(self, value_types):
        self.value_types = value_types

    def __get__(self, obj, objtype):
        for value_type in self.value_types:
            field_name = self.get_field_name(value_type)
            if getattr(obj, field_name) is not None:
                return getattr(obj, field_name)

    def __set__(self, obj, value):
        field_name, value = get_correct_value_field(value)
        setattr(obj, field_name, value)
