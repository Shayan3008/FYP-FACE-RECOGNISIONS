
from django.contrib import admin
from django.urls import path, include
from forms import views

urlpatterns = [
    path("AreaForm/",view = views.AreaForm, name="Area Form"),
    path("PoliceForm/", view = views.PoliceForm, name = "Police Form"),
    path("CameraForm/", view = views.CameraForm, name = "Camera Form")
]
