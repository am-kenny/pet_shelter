from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='welcome'),
    path('contacts', views.contacts, name='contacts')
]
