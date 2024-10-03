import os

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
import animals.models
from user.forms import UpdateUserForm, AddUserMedia
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

            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)

            return redirect("/")
        else:
            return HttpResponseNotFound("Failed to log in")


    return render(request, 'user/user_login.html', {})


@login_required
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

            return render(request, 'user/user_register.html', {"error_message": error_message}, status=409)

    return render(request, 'user/user_register.html', {})


@login_required
def user_history(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    user_schedule = animals.models.Schedule.objects.filter(user=request.user)

    return render(request, 'user/user_history.html', {"schedules": user_schedule})


@login_required
def edit_profile(request):
    form = UpdateUserForm(request.POST or None, instance=request.user)
    if form.is_valid():
        form.save()
        return redirect('user')

    return render(request, 'user/edit.html', {"form": form})


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

    form = AddUserMedia()
    main_image = request.user.usermedia_set.filter(main=True).first()
    all_images = request.user.usermedia_set.filter(main=False).all()

    return render(request, 'user/images.html', {"form": form,
                                                "main_image": main_image,
                                                "user_images": all_images})


@login_required
def set_main_image(request, user_image_id):
    if request.method == 'POST':
        old_main_image = request.user.usermedia_set.filter(main=True).first()
        if old_main_image:
            old_main_image.main = False
            old_main_image.save()
        user_image = UserMedia.objects.get(id=user_image_id)
        user_image.main = True
        user_image.save()

    return redirect('user_images')


@login_required
def delete_user_image(request, user_image_id):
    if request.method == 'POST':
        user_image = UserMedia.objects.get(id=user_image_id)
        if len(user_image.media) > 0:
            os.remove(user_image.media.path)
        user_image.delete()
    return redirect('user_images')
