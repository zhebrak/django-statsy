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
    list_display = ('__unicode__', 'object_value', 'user')
    search_fields = ('user__username', 'text_value', 'float_value', 'url')
    list_filter = ('group', 'event')
    date_hierarchy = 'created_at'
    list_select_related = ('group', 'event', 'user')
    ordering = ('-created_at',)

    def object_value(self, obj):
        return obj.value

    object_value.short_description = 'Value'


admin.site.register(StatsyGroup, StatsyGroupAdmin)
admin.site.register(StatsyEvent, StatsyEventAdmin)
admin.site.register(StatsyObject, StatsyObjectAdmin)
