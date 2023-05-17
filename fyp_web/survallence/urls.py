"""fyp_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from survallence import views

urlpatterns = [
    path("", view=views.index, name="survallence"),
    path("video/", view=views.video, name="video"),
    path("image/", view=views.input, name="input"),  # POST IMAGES INPUT
    path("face/", view=views.face, name="input"),
    path("cookie/",view = views.cookie, name = "csrftoken"),
    path("alertvideo/<int:id>/", view = views.alertVideo, name = "Alert Video"),
    path("test/", view=views.Test, name="Test Model")
    # path("coordinates/", view=views.GetCoordinates, name="Get Coordinates")
]
