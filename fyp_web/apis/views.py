import json
import os
from random import randint
import django
from django.http import FileResponse, HttpResponse
from django.shortcuts import render
from area.models import Area
from cameras.models import Camera
from coordinates.models import Coordinates
from metaData.models import metadata
from policemans.models import policeman
from shared.Shared_Methods import Shared_Methods
from wsgiref.util import FileWrapper

from users.models import ForgotPassword, Users

from django.conf import settings
from django.core.mail import send_mail


# Create your views here.

# Temporary View To check Data in DB and return All Rows in DB
def GetData(request):
    sharedMethods = Shared_Methods()
    # metadata1 = metadata(camera_id = Camera.objects.get(id = 1))
    # metadata1.save()
    # Coordinates.objects.get(id = 4).delete()
    return HttpResponse(sharedMethods.SendModelDataApiHelper(Users))

def ChangePass(request):
    if request.method == "POST":
        body = json.loads(request.body)
        Email = body["email"]
        user = Users.objects.filter(email=Email)[0]
        user.password = body["password"]
        ForgotPassword.objects.filter(userId = user.id).delete()
        user.save()
        return HttpResponse('Password Change')

def ForgotPass(request):
    if request.method == "POST":
        body = json.loads(request.body)
        Email = body["email"]
        print(Email)
        code = randint(100000,999999)
        userId = Users.objects.filter(email=Email)[0].id
        subject = 'Code  to recover Password' 
        message = 'This is ur Code for recovering pass:' + str(code)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['k190367@nu.edu.pk', ]
        send_mail( subject, message, email_from, recipient_list )
        password = ForgotPassword(userId = userId, resetCode = code)
        password.save()
        return HttpResponse('MAIL SENT')

# Api To Add Camera
def AddCamera(request):
    sharedMethods = Shared_Methods()
    if request.method == "POST":
        file_name = "/static/CameraVideos/" + request.FILES["file"].name
        area = Area.objects.get(id = request.POST.get("AreaId"))
        coordinate = Coordinates(latitude = request.POST.get("latitude"),longitude = request.POST.get("longitude"),area = area)
        sharedMethods.HandleUploadFile("static/CameraVideos/", request.FILES["file"])
        coordinate.save()
        camera = Camera(cameraLocation=coordinate,cameraVideo = file_name)
        camera.save()
        return HttpResponse("Camera And Location Added!!")
    elif request.method == "PUT":
        camera = Camera.objects.get(id = request.POST.get("id"))
        coordinate = camera.cameraLocation
        coordinate.latitude = request.POST.get("latitude")
        coordinate.longitude = request.POST.get("longitude")
        
        area = Area.objects.get(id = request.POST.get("AreaId"))
        coordinate.area = area
        coordinate.save()
        camera.cameraLocation = coordinate
        camera.save()
        print(camera.cameraLocation.area.Area_name)
        return HttpResponse(camera.cameraLocation.area.Area_name)
    elif request.method == "DELETE":
        DataBody = json.loads(request.body)
        Camera.objects.get(id = DataBody["CameraId"]).delete()
        return HttpResponse("Camera Deleted")


   


def DeleteData(request):
    sharedMethods = Shared_Methods()
    return HttpResponse(sharedMethods.DeleteModelDataApiHelper(ForgotPassword))

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
    print(Data_List)
    return HttpResponse(json.dumps(Data_List))


# Api to send video to Police men
def SendVideo(request):
    if request.method == "POST":
        data = json.loads(request.body)
        file_path = os.path.join("static", data["FileName"])
        file_wrapper = FileWrapper(open(file_path, 'rb'))
        response = FileResponse(file_wrapper, content_type='video/mp4')
        response['Content-Disposition'] = 'attachment; filename="myvideo.mp4"'
        response['Content-Length'] = os.path.getsize(file_path)
        return response


# Api to SignUp User
def UserSignUp(request):
    if request.method == "POST":
        userData = json.loads(request.body)
        # Assuming all the exception handling is done in Flutter App
        Users(name=userData["name"], email=userData["email"],
            password=userData["password"]).save()
        return HttpResponse("Congrats Ur Account Is Created")

# Api to Login User


def UserLogin(request):
    if request.method == "POST":
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
# mainCamId id for MainCam
# camId for 1st Camera
# camId2 for 2nd Camera
# }
def AddCameraLinks(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        print(data)
        print(len(data["camId2"]) > 0)
        mainCamera = Camera.objects.get(id=data["mainCamId"])
        if len(data["camId"]) > 0:
            camera1 = Camera.objects.get(id = data["camId"])
        if len(data["camId2"]) > 0:
            camera2 = Camera.objects.get(id=data["camId2"])
        if len(data["camId"]) > 0:
            mainCamera.cameraClose = camera1
            if camera1.cameraClose == None:
                camera1.cameraClose = mainCamera
            else:
                camera1.cameraClose2 = mainCamera
        if len(data["camId2"]) > 0:
            mainCamera.cameraClose2 = camera2
            if camera2.cameraClose == None:
                camera2.cameraClose = mainCamera
            else:
                camera2.cameraClose2 = mainCamera
        mainCamera.save()
        if len(data["camId"]) > 0:
            camera1.save()
        if len(data["camId2"]) > 0:
            camera2.save()
        return HttpResponse("Camera Links Added!!!!")

#Api to AddPolice
#BODY{
# email: email for police
# password: password for police
# }
def PoliceLogin(request):
    if request.method == "POST":
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
    

def GetCameraById(request,id):
    camera = Camera.objects.get(id = id)
    # print(camera.cameraLocation.area.Area_name)
    dict1 = {
        "id":id,
        "long":camera.cameraLocation.longitude,
        "lat":camera.cameraLocation.latitude,
        "area":camera.cameraLocation.area.id,
        "cameraLink":camera.cameraClose,
        "cameraLink2":camera.cameraClose2
    }
    return HttpResponse(json.dumps(dict1))


#text {body}
#file {pdf,doc,video,audio,image} blob