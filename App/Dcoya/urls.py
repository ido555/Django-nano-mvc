from django.urls import path

from . import views

urlpatterns = [
    path('register', views.registerClient, name="register"),
    # path('getAllClients', views.getAllClients, name="getAllClients"),
]