from django.shortcuts import render


def index(request):  # TODO
    return render(request, 'main/index.html', {})


def contacts(request):  # TODO
    return render(request, 'main/contacts.html', {})
