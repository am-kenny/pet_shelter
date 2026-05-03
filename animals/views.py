from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.templatetags.static import static

import animals.models
import animals.utils
from blog.forms import AnimalFeedbackForm


def index(request):  # TODO photos
    all_animals = animals.models.Animal.objects.all()
    return render(request, "animals/index.html", {"animals": all_animals})


def animal(request, animal_id: int):  # TODO more photos
    one_animal = get_object_or_404(animals.models.Animal, pk=animal_id)
    form = AnimalFeedbackForm()
    main_media = one_animal.animalmedia_set.filter(is_main=True).first()
    if main_media:
        image_url = main_media.media.url
    else:
        image_url = static("images/pet.png")
    return render(
        request,
        "animals/animal.html",
        {"form": form, "animal": one_animal, "image_url": image_url},
    )


@login_required
def schedule(request):  # TODO  confirmation
    if request.method == "POST":
        animal_id = request.POST.get("animal_id")
        if not animals.models.Animal.objects.filter(id=animal_id).exists():
            raise Http404("Animal does not exist")

        selected_date = request.POST.get("selected_date")
        try:
            desired_hours = int(request.POST.get("duration_hours"))
            desired_minutes = int(request.POST.get("duration_minutes"))
        except TypeError, ValueError:
            desired_hours = None
            desired_minutes = None

        if all([animal_id, selected_date, desired_hours or desired_minutes]):
            animal_schedule = animals.models.Schedule.objects.filter(
                animal_id=animal_id, start_time__date=selected_date
            ).all()

            available_times = get_available_times(
                animal_schedule, desired_hours, desired_minutes
            )

            selected_time_slot = request.POST.get("selected_slot")
            if selected_time_slot in available_times:
                current_user_id = request.user.id
                start_time, end_time = animals.utils.create_booked_time(
                    selected_date, selected_time_slot, desired_hours, desired_minutes
                )
                animals.models.Schedule.objects.create(
                    start_time=start_time,
                    end_time=end_time,
                    animal_id=animal_id,
                    user_id=current_user_id,
                )
                return render(request, "animals/success.html", {})

    all_animals = animals.models.Animal.objects.all()
    animal_id = request.GET.get("animal_id")
    selected_date = request.GET.get("date")
    try:
        desired_hours = int(request.GET.get("duration_hours"))
        desired_minutes = int(request.GET.get("duration_minutes"))
    except TypeError, ValueError:
        desired_hours = None
        desired_minutes = None

    if all([animal_id, selected_date, desired_hours or desired_minutes]):
        if not animals.models.Animal.objects.filter(id=animal_id).exists():
            raise Http404("Animal does not exist")

        animal_schedule = animals.models.Schedule.objects.filter(
            animal_id=animal_id, start_time__date=selected_date
        ).all()

        available_times = get_available_times(
            animal_schedule, desired_hours, desired_minutes
        )

        return render(
            request,
            "animals/schedule.html",
            {
                "schedules": animal_schedule,
                "available_slots": available_times,
                "selected_date": selected_date,
                "desired_hours": desired_hours,
                "desired_minutes": desired_minutes,
                "animal_id": animal_id,
            },
        )

    context = {"animals": all_animals}
    if animal_id and animals.models.Animal.objects.filter(id=animal_id).exists():
        context["preselected_animal_id"] = int(animal_id)

    return render(request, "animals/schedule.html", context)


def transform_schedule(animal_schedule):
    return [
        (booked_slot.start_time, booked_slot.end_time)
        for booked_slot in animal_schedule
    ]


def get_available_times(animal_schedule, desired_hours, desired_minutes):
    booked_slots = transform_schedule(animal_schedule)
    available_times = animals.utils.available_booking_times(
        booked_slots, desired_hours, desired_minutes
    )
    return available_times


@login_required
def cancel_schedule_slot(request, schedule_slot_id: int):
    if request.method == "POST":
        if (
            schedule_slot_id
            and animals.models.Schedule.objects.filter(id=schedule_slot_id).exists()
        ):
            schedule_slot = animals.models.Schedule.objects.get(id=schedule_slot_id)
            if schedule_slot.user_id == request.user.id:
                schedule_slot.delete()
    return redirect("user_history")
