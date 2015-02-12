# coding: utf-8

from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from example.models import Post

import statsy

from statsy.mixins import WatchMixin


@statsy.watch(group='index', event='page_view', value='123.1')
def index(request):
    post_list = Post.objects.all()

    return render_to_response('example/index.html', {'post_list': post_list})


@login_required
def get_post(request, post_id):
    post = get_object_or_404(Post.objects.all(), pk=post_id)

    statsy.send(
        group='post', event='page_view', user=request.user,
        url=request.path, related_object=post
    )

    return render_to_response('example/post.html', {'post': post})


class AboutView(WatchMixin, TemplateView):
    template_name = 'example/about.html'

    watch_group = 'info'
    watch_event = 'page_view'
