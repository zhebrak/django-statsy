# coding: utf-8

from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=50, verbose_name='title')
    content = models.TextField(verbose_name='content')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created at')

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ('-created_at',)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('get_post', kwargs={'post_id': self.pk})
