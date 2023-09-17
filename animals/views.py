from django.shortcuts import render


def index(request):
    return render(request, 'animals/index.html', {})


def animal(request):
    return render(request, 'animals/animal.html', {})


def schedule(request):
    return render(request, 'animals/schedule.html', {})
