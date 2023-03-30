import json
import os
import django
from django.http import FileResponse, HttpResponse
from django.shortcuts import render
from area.models import Area
from cameras.models import Camera
from coordinates.models import Coordinates
from policemans.models import policeman
from shared.Shared_Methods import Shared_Methods
from wsgiref.util import FileWrapper

from users.models import Users

# Create your views here.

# Temporary View To check Data in DB and return All Rows in DB
def GetData(request):
    sharedMethods = Shared_Methods()
    # Coordinates.objects.get(id = 4).delete()
    return HttpResponse(sharedMethods.SendModelDataApiHelper(policeman))


# Api To Add Camera
def AddCamera(request):
    DataBody = json.loads(request.body)
    if request.method == "POST":
        area = Area.objects.get(id = DataBody["AreaId"])
        coordinate = Coordinates(latitude = DataBody["latitude"],longitude = DataBody["longitude"],area = area)
        coordinate.save()
        camera = Camera(cameraLocation=coordinate)
        camera.save()
        return HttpResponse("Camera And Location Added!!")
    elif request.method == "PUT":
        camera = Camera.objects.get(id = DataBody["id"])
        camera.latitude = DataBody["latitude"]
        camera.longitude = DataBody["longitude"]
        area = Area.objects.get(id = DataBody["AreaId"])
        camera.area = area
        camera.save()
        return HttpResponse("Camera Details Updated")
    elif request.method == "DELETE":
        Camera.objects.get(id = DataBody["CameraId"]).delete()
        return HttpResponse("Camera Deleted")


   


def DeleteData(request):
    sharedMethods = Shared_Methods()
    return HttpResponse(sharedMethods.DeleteModelDataApiHelper(Users))

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
    file_path = os.path.join("static", data["FileName"])
    file_wrapper = FileWrapper(open(file_path, 'rb'))
    response = FileResponse(file_wrapper, content_type='video/mp4')
    response['Content-Disposition'] = 'attachment; filename="myvideo.mp4"'
    response['Content-Length'] = os.path.getsize(file_path)
    return response


# Api to SignUp User
def UserSignUp(request):
    userData = json.loads(request.body)
    # Assuming all the exception handling is done in Flutter App
    Users(name=userData["name"], email=userData["email"],
          password=userData["password"]).save()
    return HttpResponse("Congrats Ur Account Is Created")

# Api to Login User


def UserLogin(request):
    requestData = json.loads(request.body)
    user = Users.objects.filter(email=requestData["email"])
    if len(user) > 0:
        if user[0].password != requestData["password"]:
            return HttpResponse("Wrong Password", status=404)
        return HttpResponse(json.dumps({
            "name":user[0].name,
        }))
    else:
        return HttpResponse("Wrong Email ", status=404)


# Api to Add PoliceMan
def AddPoliceman(request):
    requestData = json.loads(request.body)
    if request.method == "POST":
        # print(requestData)
        policeman(email=requestData["email"], password=requestData["password"],
                area=Area.objects.get(id=requestData["area"])).save()
        return HttpResponse("Police Added")
    elif request.method == "PUT":
        police = policeman.objects.get(id = requestData["id"])
        police.email = requestData["email"]
        police.password = requestData["password"]
        area=Area.objects.get(id=requestData["area"])
        police.area = area
        return HttpResponse("Police Updated")
    elif request.method == "DELETE":
        policeman.objects.get(id = requestData["id"]).delete()
        return HttpResponse("Police Deleted")



def GetCookie(request):
    return HttpResponse(json.dumps(
            {
            "cookie":django.middleware.csrf.get_token(request)
            ,}
        ,)
    ,)

# Api to Link Cameras
# Body:{
# camId for 1st Camera
# camLink number 1 or 2 for 1st or 2nd link for first camera
# camId2 for 2nd Camera
# camLink2 number 1 or 2 for 1st or 2nd link for second camera
# }
def AddCameraLinks(request):
    data = json.loads(request.body)
    camera1 = Camera.objects.get(id=data["camId"])
    camera2 = Camera.objects.get(id=data["camId2"])
    if data["camLink"] == 1:
        camera1.cameraClose = camera2
    else:
        camera1.cameraClose2 = camera2
    if data["camLink2"] == 1:
        camera2.cameraClose = camera1
    else:
        camera2.cameraClose2 = camera1
    camera1.save()
    camera2.save()
    return HttpResponse("Camera Links Added!!!!")

#Api to AddPolice
#BODY{
# email: email for police
# password: password for police
# }
def PoliceLogin(request):
    requestData = json.loads(request.body)
    policemanData = policeman.objects.filter(email=requestData["email"])
    if len(policemanData) > 0:
        if policemanData[0].password != requestData["password"]:
            return HttpResponse("Wrong Password", status=404)
        return HttpResponse("Logged In")
    else:
        return HttpResponse("Wrong Email ", status=404)


def AddArea(request):
    # Add Api
    if request.method == "POST":
        requestData = json.loads(request.body)
        print(requestData)
        area = Area(Area_name = requestData["Area_Name"])
        area.save()
        return HttpResponse("Added Area")
    # Update Api
    elif request.method == "PUT":
        requestData = json.loads(request.body)
        area = Area.objects.get(id = requestData["id"])
        area.Area_name = requestData["Area_Name"]
        area.save()
        return HttpResponse("Updated Area")
    # Delete Api
    elif request.method == "DELETE":
        requestData = json.loads(request.body)
        area = Area.objects.get(id = requestData["id"]).delete()
        return HttpResponse("Deleted Area")
    

#text {body}
#file {pdf,doc,video,audio,image} blob