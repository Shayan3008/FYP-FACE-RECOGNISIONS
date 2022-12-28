from django.shortcuts import render, HttpResponse
from models.face.face import Face

# Create your views here.


def index(request):
    with open("static/project.mp4", "rb") as f:
        video = f.read()
    with open("static/file.mp4", "wb+") as destination:
        destination.write(video)
    return render(request, "admin/control.html")


def video(request):
    handleUploadFile("static/temp/", request.FILES["vid"])
    print(request.POST.get("input")[1:])
    # face = Face(request.POST.get("input")[1:])
    # input_embedding = face.embedding_extractor(face.inputImage, face.model)
    # video_path = face.play_video(
    #     "static/temp/"+request.FILES["vid"].name, input_embedding)
    return HttpResponse("videos")


def input(request):
    fileName = "/static/input/" + request.FILES["input"].name
    handleUploadFile("static/input/", request.FILES["input"])
    print(fileName)
    return HttpResponse(fileName)


def handleUploadFile(name, f):
    with open(name + f.name, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)
