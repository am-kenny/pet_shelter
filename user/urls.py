from tempfile import template

from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView)
from django.urls import path

from . import views

urlpatterns = [
    path('register', views.user_register, name='register'),
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),

    path('reset_password', PasswordResetView.as_view(template_name='user/auth/password_reset.html'), name='password_reset'),
    path('reset_password_done', PasswordResetDoneView.as_view(template_name='user/auth/password_reset_done.html'), name='password_reset_done'),
    path('reset_password_confirm/<uidb64>/<token>', PasswordResetConfirmView.as_view(template_name='user/auth/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset_password_complete', PasswordResetCompleteView.as_view(template_name='user/auth/password_reset_complete.html'), name='password_reset_complete'),

    path('history', views.user_history, name='user_history'),

    path('profile', views.index, name='user'),
    path('profile/edit', views.edit_profile, name='edit_profile'),
    path('profile/images', views.user_images, name='user_images'),
    path('profile/images/set_main_image/<int:user_image_id>/', views.set_main_image, name='set_main_image'),
    path('profile/images/delete_user_image/<int:user_image_id>/', views.delete_user_image, name='delete_user_image'),
]
