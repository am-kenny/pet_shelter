from django.shortcuts import render


def index(request):
    return render(request, 'user/index.html', {})


def user_login(request):
    return render(request, 'user/user_login.html', {})


def user_logout(request):
    return render(request, 'user/user_logout.html', {})


def user_register(request):
    return render(request, 'user/user_register.html', {})


def user_history(request):
    return render(request, 'user/user_history.html', {})
