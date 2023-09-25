from django.shortcuts import render
import animals.models
import animals.utils
from blog.forms import AnimalFeedbackForm


def index(request):  # TODO photos
    all_animals = animals.models.Animal.objects.all()
    return render(request, 'animals/index.html', {"animals": all_animals})


def animal(request, animal_id):  # TODO feedback form
    if request.method == "POST":
        form = AnimalFeedbackForm(request.POST)
        if form.is_valid():
            user = request.user
            this_animal = animals.models.Animal.objects.get(id=animal_id)
            feedback_instance = form.save(commit=False)
            feedback_instance.user = user
            feedback_instance.animal = this_animal
            feedback_instance.save()
    form = AnimalFeedbackForm()
    one_animal = animals.models.Animal.objects.get(id=animal_id)
    return render(request, 'animals/animal.html', {"form": form, "animal": one_animal})


def schedule(request):
    all_animals = animals.models.Animal.objects.all()
    animal_id = request.GET.get("animal_id")
    try:
        desired_hours = int(request.GET.get("duration_hours"))
        desired_minutes = int(request.GET.get("duration_minutes"))
    except TypeError:
        desired_hours = None
        desired_minutes = None
    schedule_date = request.GET.get("date")
    if all([animal_id, schedule_date, desired_hours or desired_minutes]):
        animal_schedule = animals.models.Schedule.objects.filter(animal_id=animal_id,
                                                                 start_time__date=schedule_date).all()
        booked_times = []
        for i in animal_schedule:
            booked_times.append((i.start_time.replace(tzinfo=None), i.end_time.replace(tzinfo=None)))
        results = animals.utils.available_booking_times(booked_times, desired_hours, desired_minutes)
        return render(request, 'animals/schedule.html',
                      {"schedules": animal_schedule, "available_slots": results})
    return render(request, 'animals/schedule.html', {"animals": all_animals})
