# coding: utf-8

from datetime import datetime
from operator import itemgetter

from django.conf import settings


class Stats(object):
    DEFAULT_CATEGORY_CLASS = 'mixed'
    DECISION_THRESHOLD = 0.95

    category_class_list = ['numbers', 'action', 'text']

    @classmethod
    def classify(cls, object_list):
        object_list_count = object_list.count()
        for category_class in cls.category_class_list:
            category_count = getattr(object_list, '_{}'.format(category_class))().count()
            if cls.DECISION_THRESHOLD < category_count / float(object_list_count):
                return category_class

        return cls.DEFAULT_CATEGORY_CLASS

    @classmethod
    def get_stats(cls, object_list, aggregation_period='auto', category_class='auto'):
        if category_class == 'auto':
            category_class = cls.classify(object_list)

        return sorted(cls._stats(object_list, category_class, aggregation_period), key=itemgetter(0))

    @classmethod
    def _stats(cls, object_list, category_class, *args):
        object_list = cls._annotate_with_time(object_list)
        aggregated_data, aggregation_period = cls._get_aggregated_stats(object_list, *args)

        return getattr(cls, 'stats_{}'.format(category_class))(aggregated_data, aggregation_period)

    @staticmethod
    def _annotate_with_time(object_list):
        time_extract_sqlite = "strftime('%%Y:%%m:%%d:%%H:%%M', created_at)"
        time_extract_mysql = "DATE_FORMAT(created_at, '%%Y:%%m:%%d:%%H:%%i')"

        time_extract = time_extract_mysql
        if settings.DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3':
            time_extract = time_extract_sqlite

        return object_list.extra({"time": time_extract}).values(
                'time', 'float_value', 'text_value'
        )

    @classmethod
    def _get_aggregated_stats(cls, data, aggregation_period):
        if aggregation_period == 'auto':
            aggregation_period = cls._get_aggregation_period(data)

        aggregated_stats = dict()

        for obj in data:
            aggregated_time = cls._get_aggregated_time(obj['time'], aggregation_period)
            if aggregated_time not in aggregated_stats:
                aggregated_stats[aggregated_time] = []

            aggregated_stats[aggregated_time].append(obj)

        return aggregated_stats.items(), aggregation_period

        # now = datetime.now()
        #
        # aggregated_periods = [
        #     cls.get_aggregated_time(
        #         '{0}:{1}:{2}'.format(day, minute / 60, minute % 60),
        #         aggregation_period
        #     )
        #     for day in range(start.day, now.day + 1)
        #     for minute in range(0, 60 * 24, aggregation_period)
        # ]
        #
        # last_period = cls.get_aggregated_time(
        #     '{0}:{1}:{2}'.format(now.day, now.hour, now.minute),
        #     aggregation_period
        # )
        #
        # for category, data in aggregated_stats.items():
        #     consecutive_null_periods = []
        #     for period in aggregated_periods:
        #         if period >= last_period:
        #             data[period] = None
        #
        #         elif period not in data:
        #             consecutive_null_periods.append(period)
        #             if len(consecutive_null_periods) == 10:
        #                 for null_period in consecutive_null_periods:
        #                     data[null_period] = None
        #
        #                 consecutive_null_periods = []
        #
        #             else:
        #                 data[period] = 0
        #
        #         else:
        #             consecutive_null_periods = []
        #             data[period] /= float(aggregation_period) / average_by
        #
        #     aggregated_stats[category] = sorted(data.items())
        #
        # return aggregated_stats

    @classmethod
    def stats_numbers(cls, data):
        return cls.stats_average(data, 'float_value')

    @classmethod
    def stats_action(cls, data, period):
        return cls.stats_count(data, period)

    @classmethod
    def stats_text(cls, data, period):
        return cls.stats_count(data, period)

    @classmethod
    def stats_mixed(cls, data, period):
        return cls.stats_count(data, period)

    @staticmethod
    def stats_average(data, key):
        return [(time, sum([float(obj[key]) for obj in stats]) / len(stats)) for time, stats in data]

    @staticmethod
    def stats_count(data, period):
        return [(time, len(stats) / float(period)) for time, stats in data]

    @staticmethod
    def _get_aggregated_time(time_string, aggregation_period):
        year, month, day, hours, minutes = time_string.split(':')
        aggregated_minutes = int(float(hours) * 60 + float(minutes)) // aggregation_period

        day = ('0' + day)[-2:]
        hours = ('0' + str(aggregated_minutes * aggregation_period // 60))[-2:]
        minutes = ('0' + str((aggregated_minutes * aggregation_period) % 60))[-2:]

        return ':'.join([year, month, day, hours, minutes])

    @staticmethod
    def _get_aggregation_period(data):
        sorted_data = sorted(data, key=lambda item: item['time'])
        start = datetime.strptime(sorted_data[0]['time'], '%Y:%m:%d:%H:%M')
        end = datetime.strptime(sorted_data[-1]['time'], '%Y:%m:%d:%H:%M')

        period_in_days = (end - start).days

        if period_in_days <= 2:
            return 15  # aggregate by 15 minutes

        if period_in_days <= 10:
            return 90

        if period_in_days <= 50:
            return 6 * 60

        if period_in_days <= 150:
            return 12 * 60

        return 24 * 60
