# coding: utf-8

from statsy.core import Statsy


_statsy = Statsy()

send = _statsy.send
watch = _statsy.watch
get_send_params = _statsy.get_send_params

objects = Statsy.objects
groups = Statsy.groups
events = Statsy.events

