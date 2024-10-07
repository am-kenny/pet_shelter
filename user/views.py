import os

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
import animals.models
from user.forms import UpdateUserForm, AddUserMedia, RegistrationForm
from user.models import UserMedia


@login_required
def index(request):
    if request.user.usermedia_set.filter(main=True).exists():
        image_url = request.user.usermedia_set.filter(main=True).first().media.url
    else:
        image_url = "/user_images/user.png"

    return render(request, 'user/index.html', {"image_url": image_url})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('welcome')

    if request.method == 'POST':
        user = authenticate(
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )
        if user is not None:
            login(request, user)
            return redirect(request.GET.get('next', 'welcome'))
        else:
            return HttpResponseNotFound("Failed to log in")

    return render(request, 'user/user_login.html', {})


@login_required
def user_logout(request):
    logout(request)
    return redirect("login")


def user_register(request):
    if request.user.is_authenticated:
        return redirect('welcome')

    if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('login')

    return render(request, 'user/user_register.html', {"form": RegistrationForm()})


@login_required
def user_history(request):
    user_schedule = animals.models.Schedule.objects.filter(user=request.user)
    return render(request, 'user/user_history.html', {"schedules": user_schedule})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UpdateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user')

    return render(request, 'user/edit.html', {"form": UpdateUserForm()})


@login_required
def user_images(request):
    if request.method == 'POST':
        form = AddUserMedia(request.POST, request.FILES)
        if form.is_valid():
            new_image = form.save(commit=False)
            new_image.main = False
            new_image.user = request.user
            new_image.save()

            return redirect('user_images')

    main_image = request.user.usermedia_set.filter(main=True).first()
    all_images = request.user.usermedia_set.filter(main=False).all()

    return render(request, 'user/images.html', {"form": AddUserMedia(),
                                                "main_image": main_image,
                                                "user_images": all_images})


@login_required
def set_main_image(request, user_image_id):
    if request.method == 'POST':
        previous_main_image = request.user.usermedia_set.filter(main=True).first()
        if previous_main_image:
            previous_main_image.main = False
            previous_main_image.save()
        user_image = UserMedia.objects.get(id=user_image_id)
        user_image.main = True
        user_image.save()

    return redirect('user_images')


@transaction.atomic
@login_required
def delete_user_image(request, user_image_id):
    if request.method == 'POST':
        if not request.user.usermedia_set.filter(id=user_image_id).exists():
            return redirect('user_images')
        user_image = request.user.usermedia_set.filter(id=user_image_id).first()

        if user_image.media:
            os.remove(user_image.media.path)
        user_image.delete()
    return redirect('user_images')
