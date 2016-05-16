# coding: utf-8

from django.contrib import admin

from statsy.models import StatsyGroup, StatsyEvent, StatsyObject

from django.contrib.admin.views.main import ChangeList


class StatsyGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('is_active',)


class StatsyEventAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('is_active',)


class ChangeListWithoutPkOrdering(ChangeList):
    """
    Django adds -pk sort key by default
    """
    def get_ordering(self, request, queryset):
        ordering = super(ChangeListWithoutPkOrdering, self).get_ordering(request, queryset)
        if '-pk' in ordering:
            ordering.remove('-pk')
        return ordering


class StatsyObjectAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'object_value', 'duration', 'url')
    search_fields = ('user__username', 'value', 'url')
    list_filter = ('group__name', 'event__name', 'label')
    date_hierarchy = 'created_at'
    list_select_related = ('group', 'event', 'user')
    ordering = ('-created_at',)

    def object_value(self, obj):
        return obj.value

    object_value.short_description = 'Value'

    def get_changelist(self, request, **kwargs):
        return ChangeListWithoutPkOrdering


admin.site.register(StatsyGroup, StatsyGroupAdmin)
admin.site.register(StatsyEvent, StatsyEventAdmin)
admin.site.register(StatsyObject, StatsyObjectAdmin)
