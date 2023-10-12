from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
import animals.models
from user.forms import UpdateUserForm


def index(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    if request.user.usermedia_set.filter(user_id=request.user.id).exists():
        image_url = request.user.usermedia_set.first().media.url
    else:
        image_url = ""
    return render(request, 'user/index.html', {"image_url": image_url})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(
            username=username,
            password=password
        )
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            return HttpResponseNotFound("Failed to log in")
    return render(request, 'user/user_login.html', {})


def user_logout(request):
    if not request.user.is_authenticated:
        return redirect('/')
    logout(request)
    return redirect("/login")


def user_register(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            new_user = User.objects.create_user(username, email, password)
            new_user.save()
            return redirect('/login')
        except Exception:
            error_message = "Username already exists"
            return render(request, 'user/user_register.html', {"error_message": error_message}, status=409)
    return render(request, 'user/user_register.html', {})


def user_history(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    user_schedule = animals.models.Schedule.objects.filter(user=request.user)
    return render(request, 'user/user_history.html', {"schedules": user_schedule})


def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    if request.user.usermedia_set.filter(user_id=request.user.id).exists():
        image_url = request.user.usermedia_set.first().media.url
    else:
        image_url = ""
    form = UpdateUserForm(request.POST or None, instance=request.user)

    if form.is_valid():
        form.save()
        return redirect('user')
    return render(request, 'user/edit.html', {"image_url": image_url, "form": form})
