# coding: utf-8

from django.contrib import admin

from example.models import Post


class PostAdmin(admin.ModelAdmin):
    pass


admin.site.register(Post, PostAdmin)

