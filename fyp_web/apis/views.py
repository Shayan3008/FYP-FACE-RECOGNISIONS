import json
import os
from django.http import FileResponse, HttpResponse
from django.shortcuts import render
from cameras.models import Camera
from coordinates.models import Coordinates
from shared.Shared_Methods import Shared_Methods
from wsgiref.util import FileWrapper

# Create your views here.


def GetCoordinates(request):
    sharedMethods = Shared_Methods()
    return HttpResponse(sharedMethods.SendModelDataApiHelper(Camera))


# Api to join Data from Camera and Coordinates
def getLocationWithCameraId(request):
    location = Camera.objects.all()
    Data_List = []
    for i in location:
        camera_location = i.cameraLocation
        Data_List.append({
            "id": i.id,
            "longitude": camera_location.longitude,
            "latitude": camera_location.latitude,
        })
    return HttpResponse(json.dumps(Data_List))


# Api to send video to Police men 
def SendVideo(request):
    data = json.loads(request.body)
    file_path = os.path.join("static",data["FileName"])
    file_wrapper = FileWrapper(open(file_path, 'rb'))
    response = FileResponse(file_wrapper, content_type='video/mp4')
    response['Content-Disposition'] = 'attachment; filename="myvideo.mp4"'
    response['Content-Length'] = os.path.getsize(file_path)
    return response
