# coding: utf-8

from django.core.urlresolvers import reverse
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ('-created_at',)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('get_post', kwargs={'post_id': self.pk})
