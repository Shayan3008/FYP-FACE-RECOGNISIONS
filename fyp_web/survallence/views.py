from django.shortcuts import render, HttpResponse
from models.face.face import Face
# Create your views here.


def index(request):
    print(request)
    return render(request,"admin/control.html")

def video(request):
    handleUploadFile(request.FILES["vid"])
    return HttpResponse("This is video Path !!!")

def handleUploadFile(f):
    with open("static/temp/" + f.name, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)