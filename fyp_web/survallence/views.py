from django.shortcuts import render, HttpResponse
from models.face.face import Face
from models.gait.gait import load_model
from models.gait.gait import main
from survallence.models import Coordinates
import json
# Create your views here.


def index(request):  # Main WebPage Url
    # with open("static/project.mp4", "rb") as f:
    #     video = f.read()
    # with open("static/file.mp4", "wb+") as destination:
    #     destination.write(video)
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
    return HttpResponse("shayan")


def input(request):  # Helper function to save input file and respond files name
    fileName = "/static/input/" + request.FILES["input"].name
    handleUploadFile("static/input/", request.FILES["input"])
    return HttpResponse(fileName)


def handleUploadFile(name, f):  # function to Save file sent from HTTP
    with open(name + f.name, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return name+f.name


def face(request):
    return render(request, "admin/face.html")


def postData(request): # function to push temperory data in db
    print(list(Coordinates.objects.values_list()))
    return HttpResponse(json.dumps(list(Coordinates.objects.values())))

def GetCoordinates(request):
    return HttpResponse(json.dumps(list(Coordinates.objects.values())))
