from django.shortcuts import render
from .models import Post


def index(request):
    posts = Post.objects.all()

    return render(request, 'posts/index.html', {'posts': posts})


def post_detail(request, slug):

    post = Post.objects.get(slug=slug)

    return render(request, 'posts/post_detail.html', {'post': post})
