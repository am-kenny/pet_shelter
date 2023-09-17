from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='blog'),
    path('<int:post_id>', views.blog_post, name='blog_post'),
    path('feedbacks', views.feedbacks, name='feedbacks')
]
