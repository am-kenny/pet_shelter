from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
import animals.models


def index(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    return render(request, 'user/index.html', {})


def user_login(request):
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
            return HttpResponse("Failed to log in")
    if request.user.is_authenticated:
        return redirect('/')
    return render(request, 'user/user_login.html', {})


def user_logout(request):
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
            return render(request, 'user/user_register.html', {"error_message": error_message})
    return render(request, 'user/user_register.html', {})


def user_history(request):
    user_schedule = animals.models.Schedule.objects.filter(user=request.user)
    return render(request, 'user/user_history.html', {"schedules": user_schedule})
