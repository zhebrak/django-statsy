# coding: utf-8

from statsy import statsy


class StatsyMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        statsy.send(
            user=request.user, group='group', event='event', url=request.path
        )
