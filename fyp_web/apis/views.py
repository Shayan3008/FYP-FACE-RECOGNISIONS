import json
from django.http import HttpResponse
from django.shortcuts import render

from coordinates.models import Coordinates
from shared.Shared_Methods import Shared_Methods


# Create your views here.


def GetCoordinates(request):
    sharedMethods = Shared_Methods()
    return HttpResponse(sharedMethods.SendModelDataApiHelper(Coordinates))


def PushTempData(request):
    list1 = [
        {"lat": 24.954026378293587, "long": 67.05843673597522, },
        {"lat": 24.946861240743132, "long": 67.05332256849731, }
    ]

    for i in list1:
        data1 = Coordinates(latitude=i["lat"], longitude=i["long"])
        data1.save()
