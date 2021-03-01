from django.urls import path

from . import views

urlpatterns = [
    path('register', views.registerClient, name="register"),
    path('echo', views.echo, name="echo"),
    path('time', views.time, name="time"),
]