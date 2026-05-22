import datetime

from django.conf import settings
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import get_object_or_404, render

import animals.booking_time
import animals.models


def send_schedule_confirmation_email(
    *,
    user_email: str,
    animal_name: str,
    start_time,
    end_time,
) -> None:
    body = (
        f"Your walk has been booked.\n\n"
        f"Animal: {animal_name}\n"
        f"Start: {start_time}\n"
        f"End: {end_time}\n\n"
        f"You can review or cancel bookings from your account history.\n"
    )
    send_mail(
        subject="Your pet shelter walk schedule",
        message=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user_email],
        fail_silently=False,
    )


def _booked_slots(
    animal_schedule: list[animals.models.Schedule],
) -> list[animals.booking_time.Timeslot]:
    return [
        animals.booking_time.Timeslot(booked_slot.start_time, booked_slot.end_time)
        for booked_slot in animal_schedule
    ]


def get_available_times(
    animal_schedule: list[animals.models.Schedule],
    booking_date: str,
    desired_hours,
    desired_minutes,
):
    booked_slots = _booked_slots(animal_schedule)
    for_date = datetime.date.fromisoformat(booking_date)
    return animals.booking_time.available_booking_times(
        booked_slots,
        desired_hours,
        desired_minutes,
        for_date=for_date,
    )


def schedule_page_response(request, *, all_animals, **context):
    base = {"animals": all_animals}
    base.update(context)
    return render(request, "animals/schedule.html", base)


def read_schedule_duration(source) -> tuple[int | None, int | None]:
    try:
        return (
            int(source.get("duration_hours")),
            int(source.get("duration_minutes")),
        )
    except TypeError, ValueError:
        return None, None


def validate_schedule_animal_id(animal_id: str) -> None:
    if animal_id and not animals.models.Animal.objects.filter(pk=animal_id).exists():
        raise Http404("Animal does not exist")


def schedule_prefill_context(
    animal_id: str,
    selected_date: str,
    desired_hours: int | None,
    desired_minutes: int | None,
) -> dict:
    ctx = {}
    if animal_id:
        ctx["preselected_animal_id"] = int(animal_id)
    if selected_date:
        ctx["selected_date"] = selected_date
    if desired_hours is not None:
        ctx["desired_hours"] = desired_hours
    if desired_minutes is not None:
        ctx["desired_minutes"] = desired_minutes
    return ctx


def schedule_filter_complete(
    animal_id: str,
    selected_date: str,
    desired_hours: int | None,
    desired_minutes: int | None,
) -> bool:
    return bool(
        animal_id
        and selected_date
        and desired_hours is not None
        and desired_minutes is not None
        and (desired_hours or desired_minutes)
    )


def schedule_booking_flow_response(
    request,
    *,
    all_animals,
    animal_id: str,
    selected_date: str,
    desired_hours: int,
    desired_minutes: int,
    selected_time_slot: str,
    confirming: bool,
):
    animal_schedule = animals.models.Schedule.objects.filter(
        animal_id=animal_id, start_time__date=selected_date
    ).all()
    available_times = get_available_times(
        animal_schedule, selected_date, desired_hours, desired_minutes
    )

    if selected_time_slot and selected_time_slot in available_times:
        booked = animals.booking_time.create_booked_time(
            selected_date, selected_time_slot, desired_hours, desired_minutes
        )
        start_time, end_time = booked.start, booked.end
        animal = get_object_or_404(animals.models.Animal, pk=animal_id)
        if confirming:
            animals.models.Schedule.objects.create(
                start_time=start_time,
                end_time=end_time,
                animal_id=animal_id,
                user_id=request.user.id,
            )
            send_schedule_confirmation_email(
                user_email=request.user.email,
                animal_name=str(animal),
                start_time=start_time,
                end_time=end_time,
            )
            return render(request, "animals/success.html", {})
        return render(
            request,
            "animals/schedule_confirm.html",
            {
                "animal": animal,
                "selected_date": selected_date,
                "selected_slot": selected_time_slot,
                "start_time": start_time,
                "end_time": end_time,
                "desired_hours": desired_hours,
                "desired_minutes": desired_minutes,
                "animal_id": animal_id,
            },
        )

    return schedule_page_response(
        request,
        all_animals=all_animals,
        show_slot_picker=True,
        available_slots=available_times,
        selected_date=selected_date,
        desired_hours=desired_hours,
        desired_minutes=desired_minutes,
        preselected_animal_id=int(animal_id),
    )


def schedule_post(request, all_animals):
    animal_id = (request.POST.get("animal_id") or "").strip()
    validate_schedule_animal_id(animal_id)

    selected_date = (request.POST.get("selected_date") or "").strip()
    desired_hours, desired_minutes = read_schedule_duration(request.POST)
    confirming = request.POST.get("confirm_schedule") == "1"
    selected_time_slot = (request.POST.get("selected_slot") or "").strip()

    if schedule_filter_complete(
        animal_id, selected_date, desired_hours, desired_minutes
    ):
        return schedule_booking_flow_response(
            request,
            all_animals=all_animals,
            animal_id=animal_id,
            selected_date=selected_date,
            desired_hours=desired_hours,
            desired_minutes=desired_minutes,
            selected_time_slot=selected_time_slot,
            confirming=confirming,
        )

    ctx = schedule_prefill_context(
        animal_id, selected_date, desired_hours, desired_minutes
    )
    return schedule_page_response(request, all_animals=all_animals, **ctx)


def schedule_get(request, all_animals):
    animal_id = (request.GET.get("animal_id") or "").strip()
    selected_date = (request.GET.get("date") or "").strip()
    desired_hours, desired_minutes = read_schedule_duration(request.GET)

    validate_schedule_animal_id(animal_id)

    ctx = schedule_prefill_context(
        animal_id, selected_date, desired_hours, desired_minutes
    )
    return schedule_page_response(request, all_animals=all_animals, **ctx)
