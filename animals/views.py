from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, redirect, render
from django.templatetags.static import static

import animals.models
import animals.schedule_booking
from blog.forms import AnimalFeedbackForm


def index(request):
    main_media = animals.models.AnimalMedia.objects.filter(is_main=True)
    all_animals = animals.models.Animal.objects.all().prefetch_related(
        Prefetch("animalmedia_set", queryset=main_media)
    )
    return render(request, "animals/index.html", {"animals": all_animals})


def animal(request, animal_id: int):
    media_qs = animals.models.AnimalMedia.objects.order_by("-is_main", "id")
    one_animal = get_object_or_404(
        animals.models.Animal.objects.prefetch_related(
            Prefetch("animalmedia_set", queryset=media_qs)
        ),
        pk=animal_id,
    )
    show_feedback_form = False
    feedback_form = None
    if request.user.is_authenticated:
        show_feedback_form = animals.models.Schedule.user_has_completed_walk(
            request.user, one_animal.pk
        )
        if show_feedback_form:
            feedback_form = AnimalFeedbackForm()
    photo_urls = [m.media.url for m in one_animal.animalmedia_set.all()]
    if not photo_urls:
        photo_urls = [static("images/pet.png")]
    return render(
        request,
        "animals/animal.html",
        {
            "animal": one_animal,
            "photo_urls": photo_urls,
            "show_feedback_form": show_feedback_form,
            "feedback_form": feedback_form,
        },
    )


@login_required
def schedule(request):
    all_animals = animals.models.Animal.objects.all()
    if request.method == "POST":
        return animals.schedule_booking.schedule_post(request, all_animals)
    return animals.schedule_booking.schedule_get(request, all_animals)


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
