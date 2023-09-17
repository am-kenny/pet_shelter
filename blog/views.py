from django.shortcuts import render


def index(request):
    return render(request, 'blog/index.html', {})


def blog_post(request):
    return render(request, 'blog/blog_post.html', {})


def feedbacks(request):
    return render(request, 'blog/feedbacks.html', {})