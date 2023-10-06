from django.http import HttpResponseNotFound
from django.shortcuts import render
import animals.models
import blog.models
from blog.forms import FeedbackForm


def index(request):
    blog_posts = blog.models.Blog.objects.all()
    return render(request, 'blog/index.html', {"blog_posts": blog_posts})


def blog_post(request, post_id):
    if blog.models.Blog.objects.filter(id=post_id).exists():
        blog_post_obj = blog.models.Blog.objects.get(id=post_id)
        return render(request, 'blog/blog_post.html', {"blog_post": blog_post_obj})
    return HttpResponseNotFound()


def feedbacks(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            form = FeedbackForm(request.POST)
            if form.is_valid():
                user = request.user
                feedback_instance = form.save(commit=False)
                feedback_instance.user = user
                feedback_instance.save()
    form = FeedbackForm()
    all_animals = animals.models.Animal.objects.all()
    animal_id = request.GET.get("animal_id")
    all_feedbacks = blog.models.Feedback.objects
    if animal_id:
        all_feedbacks = all_feedbacks.filter(animal_id=animal_id)
    results = all_feedbacks.all()
    return render(request, 'blog/feedbacks.html',
                  {"form": form, "feedbacks": results, "animals": all_animals})
