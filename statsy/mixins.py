# coding: utf-8

import statsy


class WatchMixin(object):
    watch_group = None
    watch_event = None
    watch_value = None
    watch_label = None

    def dispatch(self, request, *args, **kwargs):
        watch_map = {
            'group': self.watch_group,
            'event': self.watch_event,
            'value': self.watch_value,
            'label': self.watch_label
        }

        return statsy.watch(**watch_map)(
            super(WatchMixin, self).dispatch
        )(request, *args, **kwargs)
