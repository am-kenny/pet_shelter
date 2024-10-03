from django.urls import path

from . import views

urlpatterns = [
    path('animals', views.index, name='animals'),
    path('animals/<animal_id>', views.animal, name='animal'),
    path('schedule', views.schedule, name='schedule'),
    path('schedule/cancel/<schedule_slot_id>', views.cancel_schedule_slot, name='cancel_schedule_slot'),
]
