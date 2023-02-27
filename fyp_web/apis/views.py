import json
from django.http import HttpResponse
from django.shortcuts import render

from survallence.models import Coordinates

# Create your views here.


def GetCoordinates(request):
    return HttpResponse(json.dumps(list(Coordinates.objects.values())))
