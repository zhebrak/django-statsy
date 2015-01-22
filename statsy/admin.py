# coding: utf-8

from django.contrib import admin

from statsy.models import StatsyGroup, StatsyEvent, StatsyObject


class StatsyGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('is_active',)


class StatsyEventAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('is_active',)


class StatsyObjectAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__', 'user', 'value',
        'text_value', 'duration', 'url'
    )
    search_fields = ('user__username', 'value', 'text_value', 'url')
    list_filter = ('group__name', 'event__name', 'user', 'url')
    date_hierarchy = 'created_at'
    list_select_related = ('group', 'event', 'user')


admin.site.register(StatsyGroup, StatsyGroupAdmin)
admin.site.register(StatsyEvent, StatsyEventAdmin)
admin.site.register(StatsyObject, StatsyObjectAdmin)
