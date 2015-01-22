# coding: utf-8

from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required

from example.models import Post

from statsy import statsy


@statsy.watch(group='index', event='page_view')
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
