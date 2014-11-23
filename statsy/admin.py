# coding: utf-8

from django.contrib import admin

from statsy.models import StatsyGroup, StatsyAction, StatsyObject


class StatsyGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'enabled')
    list_editable = ('enabled',)
    list_filter = ('enabled',)


class StatsyActionAdmin(admin.ModelAdmin):
    list_display = ('name', 'enabled')
    list_editable = ('enabled',)
    list_filter = ('enabled',)


class StatsyObjectAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__', 'user', 'value',
        'text_value', 'action_object', 'duration', 'url'
    )
    search_fields = ('user__username', 'value', 'text_value', 'url')
    list_filter = ('group__name', 'action__name', 'user', 'url')
    date_hierarchy = 'created_at'
    list_select_related = ('group', 'action', 'user')


admin.site.register(StatsyGroup, StatsyGroupAdmin)
admin.site.register(StatsyAction, StatsyActionAdmin)
admin.site.register(StatsyObject, StatsyObjectAdmin)
