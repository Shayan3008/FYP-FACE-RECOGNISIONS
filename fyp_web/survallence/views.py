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


def index(request):  # Main WebPage Url
    # with open("static/project.mp4", "rb") as f:
    #     video = f.read()
    # with open("static/file.mp4", "wb+") as destination:
    #     destination.write(video)
    context = Camera.objects.all()
    return render(request, "admin/index.html", context = {"camera": context})


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

def alertVideo(request,id):
    camera = Camera.objects.get(id = id)
    context = {
        "camera":camera
    }
    return render(request,"admin/video.html",context = context)