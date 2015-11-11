# coding: utf-8


def string_is_intable(string_object):
    return string_object.isdigit()


def string_is_floatable(string_object):
    try:
        float(string_object)

    except ValueError:
        return False

    else:
        return True


def memoize(function):
    class MemoDict(dict):
        def __getitem__(self, *key):
            return dict.__getitem__(self, key)

        def __missing__(self, key):
            result = self[key] = function(*key)
            return result

    return MemoDict().__getitem__


@memoize
def get_correct_value_field(value):
    if value is None or value == 'None':
        return 'float_value', None

    if isinstance(value, (float, int)) or (isinstance(value, str) and string_is_floatable(value)):
        return 'float_value', float(value)

    try:
        value = str(value)
    except UnicodeEncodeError:
        pass

    return 'text_value', value
