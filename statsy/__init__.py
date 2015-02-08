# coding: utf-8

from statsy.core import Statsy


_statsy = Statsy()

send = _statsy.send
watch = _statsy.watch

objects = Statsy.objects
groups = Statsy.groups
events = Statsy.events
