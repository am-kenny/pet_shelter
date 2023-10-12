from django.urls import path

from . import views

urlpatterns = [
    path('profile', views.index, name='user'),
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('register', views.user_register, name='register'),
    path('history', views.user_history, name='user_history'),
    path('profile/edit', views.edit_profile, name='edit'),
]
