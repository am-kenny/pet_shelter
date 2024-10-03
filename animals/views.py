from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import animals.models
import animals.utils
from blog.forms import AnimalFeedbackForm
from django.http import HttpResponseNotFound, Http404


def index(request):  # TODO photos
    all_animals = animals.models.Animal.objects.all()
    return render(request, 'animals/index.html', {"animals": all_animals})


def animal(request, animal_id: int):  # TODO more photos
    if animals.models.Animal.objects.filter(id=animal_id).exists():
        form = AnimalFeedbackForm()
        one_animal = animals.models.Animal.objects.get(id=animal_id)
        if one_animal.animalmedia_set.filter(animal_id=animal_id, is_main=True).exists():
            image_url = one_animal.animalmedia_set.get(animal_id=animal_id, is_main=True).media.url
        else:
            image_url = "/animal_images/pet.png"
        return render(request, 'animals/animal.html', {"form": form,
                                                       "animal": one_animal,
                                                       "image_url": image_url})
    return HttpResponseNotFound()

@login_required
def schedule(request):  # TODO  confirmation
    if request.method == "POST":
        animal_id = request.POST.get('animal_id')
        if not animals.models.Animal.objects.filter(id=animal_id).exists():
            raise Http404("Animal does not exist")

        selected_date = request.POST.get('selected_date')
        try:
            desired_hours = int(request.POST.get("duration_hours"))
            desired_minutes = int(request.POST.get("duration_minutes"))
        except (TypeError, ValueError):
            desired_hours = None
            desired_minutes = None

        if all([animal_id, selected_date, desired_hours or desired_minutes]):
            animal_schedule = animals.models.Schedule.objects.filter(animal_id=animal_id,
                                                                     start_time__date=selected_date).all()

            available_times = get_available_times(animal_schedule, desired_hours, desired_minutes)

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
    except (TypeError, ValueError):
        desired_hours = None
        desired_minutes = None

    if all([animal_id, selected_date, desired_hours or desired_minutes]):
        if not animals.models.Animal.objects.filter(id=animal_id).exists():
            raise Http404("Animal does not exist")

        animal_schedule = animals.models.Schedule.objects.filter(animal_id=animal_id,
                                                                 start_time__date=selected_date).all()

        available_times = get_available_times(animal_schedule, desired_hours, desired_minutes)

        return render(request, 'animals/schedule.html', {"schedules": animal_schedule,
                                                         "available_slots": available_times,
                                                         "selected_date": selected_date,
                                                         "desired_hours": desired_hours,
                                                         "desired_minutes": desired_minutes,
                                                         "animal_id": animal_id
                                                         })

    return render(request, 'animals/schedule.html', {"animals": all_animals})


def transform_schedule(animal_schedule):
    return [(booked_slot.start_time.replace(tzinfo=None), booked_slot.end_time.replace(tzinfo=None)) for booked_slot in animal_schedule]

def get_available_times(animal_schedule, desired_hours, desired_minutes):
    booked_slots = transform_schedule(animal_schedule)
    available_times = animals.utils.available_booking_times(booked_slots, desired_hours, desired_minutes)
    return available_times

@login_required
def cancel_schedule_slot(request, schedule_slot_id: int):
    if request.method == "POST":
        if schedule_slot_id and animals.models.Schedule.objects.filter(id=schedule_slot_id).exists():
           schedule_slot = animals.models.Schedule.objects.get(id=schedule_slot_id)
           if schedule_slot.user_id == request.user.id:
                schedule_slot.delete()
    return redirect('/history')