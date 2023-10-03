from django.shortcuts import render, redirect
import animals.models
import animals.utils
from blog.forms import AnimalFeedbackForm
from django.http import HttpResponseNotFound


def index(request):  # TODO photos
    all_animals = animals.models.Animal.objects.all()
    return render(request, 'animals/index.html', {"animals": all_animals})


def animal(request, animal_id):  # TODO photo
    if request.method == "POST":
        form = AnimalFeedbackForm(request.POST)
        if form.is_valid():
            user = request.user
            this_animal = animals.models.Animal.objects.get(id=animal_id)
            feedback_instance = form.save(commit=False)
            feedback_instance.user = user
            feedback_instance.animal = this_animal
            feedback_instance.save()
    if animals.models.Animal.objects.filter(id=animal_id).exists():
        form = AnimalFeedbackForm()
        one_animal = animals.models.Animal.objects.get(id=animal_id)
        return render(request, 'animals/animal.html', {"form": form, "animal": one_animal})
    return HttpResponseNotFound()


def schedule(request):  # TODO  confirmation
    if not request.user.is_authenticated:
        return redirect('/login')
    if request.method == "POST":
        animal_id = request.POST.get('animal_id')
        selected_date = request.POST.get('selected_date')
        try:
            desired_hours = int(request.POST.get("duration_hours"))
            desired_minutes = int(request.POST.get("duration_minutes"))
        except TypeError:
            desired_hours = None
            desired_minutes = None
        if all([animal_id, selected_date, desired_hours or desired_minutes]):
            animal_schedule = animals.models.Schedule.objects.filter(animal_id=animal_id,
                                                                     start_time__date=selected_date).all()
            booked_times = []
            for i in animal_schedule:
                booked_times.append((i.start_time.replace(tzinfo=None), i.end_time.replace(tzinfo=None)))
            available_times = animals.utils.available_booking_times(booked_times, desired_hours, desired_minutes)

            selected_time_slot = request.POST.get('selected_slot')
            if selected_time_slot in available_times:
                current_user_id = request.user.id
                start_time, end_time = animals.utils.create_booked_time(selected_date, selected_time_slot,
                                                                        desired_hours,
                                                                        desired_minutes)
                new_booked_time = animals.models.Schedule.objects.create(start_time=start_time,
                                                                         end_time=end_time,
                                                                         animal_id=animal_id,
                                                                         user_id=current_user_id)
                new_booked_time.save()
                return render(request, "animals/success.html", {})
    all_animals = animals.models.Animal.objects.all()
    animal_id = request.GET.get("animal_id")
    selected_date = request.GET.get("date")
    try:
        desired_hours = int(request.GET.get("duration_hours"))
        desired_minutes = int(request.GET.get("duration_minutes"))
    except TypeError:
        desired_hours = None
        desired_minutes = None
    if all([animal_id, selected_date, desired_hours or desired_minutes]):
        animal_schedule = animals.models.Schedule.objects.filter(animal_id=animal_id,
                                                                 start_time__date=selected_date).all()
        booked_times = []
        for i in animal_schedule:
            booked_times.append((i.start_time.replace(tzinfo=None), i.end_time.replace(tzinfo=None)))
        available_times = animals.utils.available_booking_times(booked_times, desired_hours, desired_minutes)

        return render(request, 'animals/schedule.html', {"schedules": animal_schedule,
                                                         "available_slots": available_times,
                                                         "selected_date": selected_date,
                                                         "desired_hours": desired_hours,
                                                         "desired_minutes": desired_minutes,
                                                         "animal_id": animal_id
                                                         })
    return render(request, 'animals/schedule.html', {"animals": all_animals})
