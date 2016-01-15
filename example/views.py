# coding: utf-8

import time

from datetime import datetime, timedelta
from random import randint

from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.template import RequestContext
from django.views.generic import TemplateView

from example.models import Post

import statsy

from statsy.mixins import WatchMixin


@statsy.watch(group='index', event='page_view', value='123.1')
def index(request):
    populate_stats()

    post_list = Post.objects.all()

    return render_to_response('example/index.html', {'post_list': post_list}, RequestContext(request))


@login_required
def get_post(request, post_id):
    post = get_object_or_404(Post.objects.all(), pk=post_id)
    content_type = ContentType.objects.get_for_model(post.__class__)

    statsy.send(
        group='post', event='page_view', user=request.user,
        url=request.path, content_object=post
    )

    context = {
        'post': post,
        'content_type': content_type
    }

    return render_to_response('example/post.html', context, RequestContext(request))


class AboutView(WatchMixin, TemplateView):
    template_name = 'example/about.html'

    watch_group = 'info'
    watch_event = 'page_view'


def populate_stats():
    if statsy.objects.today().count() > 1000:
        return

    start = time.mktime((datetime.now() - timedelta(days=1)).timetuple())
    end = time.mktime(datetime.now().timetuple())

    for _ in range(1000):
        group = 'populated_{0}'.format(str(randint(0, 5)))
        event = 'populated_{0}'.format(str(randint(0, 5)))
        label = 'populated_{0}'.format(str(randint(0, 5)))
        timestamp = randint(start, end)

        statsy.send(
            group=group, event=event, label=label,
            created_at=datetime.fromtimestamp(timestamp)
        )
