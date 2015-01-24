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


def memoize(f):
    class Memodict(dict):
        def __getitem__(self, *key):
            return dict.__getitem__(self, key)

        def __missing__(self, key):
            ret = self[key] = f(*key)
            return ret

    return Memodict().__getitem__


@memoize
def get_correct_value_field(value):
    if isinstance(value, int) or (isinstance(value, str) and string_is_intable(value)):
        return 'int_value', int(value)

    if isinstance(value, float) or (isinstance(value, str) and string_is_floatable(value)):
        return 'float_value', float(value)

    return 'text_value', str(value)

