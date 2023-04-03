from django.shortcuts import render, HttpResponse
from area.models import Area
from cameras.models import Camera
# from models.face.face import Face
# from models.gait.gait import load_model
# from models.gait.gait import main
import json
import os
from policemans.models import policeman

from shared.Shared_Methods import Shared_Methods
from survallence.thread import ModelThread
# Create your views here.


def ViewForAreaList(request):
    shared = Shared_Methods()
    Table_Head = shared.GetAllColumnNamesFromTable(Area)
    dataList = list(Area.objects.values())
    context = {"list": dataList,"list2":Table_Head}
    return render(request, "admin/List/AreaList.html",context=context)

def ViewForPoliceList(request):
    shared = Shared_Methods()
    Table_Head = shared.GetAllColumnNamesFromTable(policeman)
    Table_Head.reverse()
    Table_Head.pop(Table_Head.index("password"))
    dataList = list(policeman.objects.values("area_id","email","id"))
    context = {"list": dataList,"list2":Table_Head}
    return render(request, "admin/List/SignupList.html",context=context)


def ViewForCameraList(request):
    location = Camera.objects.all()
    Data_List = []
    for i in location:
        camera_location = i.cameraLocation
        Data_List.append({
            "id": i.id,
            "longitude": camera_location.longitude,
            "latitude": camera_location.latitude,
        })
    Table_Head = ["id","longitude","latitude"]
    context = {"list": Data_List,"list2":Table_Head}
    return render(request, "admin/List/CameraList.html",context=context)

def index(request):  # Main WebPage Url
    # with open("static/project.mp4", "rb") as f:
    #     video = f.read()
    # with open("static/file.mp4", "wb+") as destination:
    #     destination.write(video)
    print(os.getcwd())
    return render(request, "admin/control.html")


def video(request):  # Function to Upload and give video input to Model
    # reid = load_model()
    # videoName = handleUploadFile("static/temp/", request.FILES["vid"])
    # print(request.POST.get("input")[1:])
    # face = Face(request.POST.get("input")[1:])
    # input_embedding = face.embedding_extractor(face.inputImage, face.model)
    # video_path = face.play_video(
    #     "static/temp/"+request.FILES["vid"].name, input_embedding)
    # video_path = main(reid, request.POST.get("input")[
    #                   1:], "static/temp/"+request.FILES["vid"].name)
    # return HttpResponse(video_path)
    ModelThread(request.POST.get("input")[
                      1:], "static/temp/"+request.FILES["vid"].name).start() 
    return HttpResponse("shayan")


def input(request):  # Helper function to save input file and respond files name
    fileName = "/static/input/" + request.FILES["input"].name
    # A helper class used to get multiple Shared Methods in a single class
    sharedMethods = Shared_Methods()
    sharedMethods.HandleUploadFile("static/input/", request.FILES["input"])
    return HttpResponse(fileName)


def face(request):
    return render(request, "admin/face.html")


def cookie(request):
    return render(request,"admin/cookie.html")