# coding: utf-8

from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required

from example.models import Post

from statsy import statsy


@statsy.watch(group='index', action='page_view')
def index(request):
    post_list = Post.objects.all()

    return render_to_response('example/index.html', {'post_list': post_list})


@login_required
def get_post(request, post_id):
    post = get_object_or_404(Post.objects.all(), pk=post_id)

    statsy.send(
        user=request.user, group='post', action='page_view',
        url=request.path, action_object=post
    )

    return render_to_response('example/post.html', {'post': post})
