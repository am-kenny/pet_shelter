from django.shortcuts import render
import animals.models


def index(request):  # TODO photos
    all_animals = animals.models.Animal.objects.all()
    return render(request, 'animals/index.html', {"animals": all_animals})


def animal(request, animal_id):  # TODO feedback form
    one_animal = animals.models.Animal.objects.get(id=animal_id)
    return render(request, 'animals/animal.html', {"animal": one_animal})


def schedule(request):
    all_schedule = animals.models.Schedule.objects.all()
    return render(request, 'animals/schedule.html', {"schedules": all_schedule})
