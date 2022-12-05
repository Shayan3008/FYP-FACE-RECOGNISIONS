from django.shortcuts import render, HttpResponse
# from models.face.face import Face
# Create your views here.


def index(request):
    return render(request,"admin/control.html")
