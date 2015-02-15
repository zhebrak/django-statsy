# coding: utf-8


class StatsyException(Exception):
    pass


class StatsyDisabled(StatsyException):
    pass


class AlreadyRegistered(StatsyException):
    pass

