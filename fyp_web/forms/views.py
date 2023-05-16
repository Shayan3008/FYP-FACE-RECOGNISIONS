from django.shortcuts import render

from area.models import Area
from cameras.models import Camera
from policemans.models import policeman

# Create your views here.
def AreaForm(request):
    return render(request, "admin/Forms/AreaForm.html")

def PoliceForm(request):
    police = policeman.objects.all()
    dict1 = {}
    for i in police:
        dict1[i.area.id] = 1
    
    print(police[0].area.id)
    AreaNotTaken = []
    areas = Area.objects.all()
    for i in areas:
        if i.id not in dict1:
            AreaNotTaken.append(i)
    context = {"list": AreaNotTaken}
    return render(request , "admin/Forms/PoliceSignupForm.html",context = context)

def CameraForm(request):
    context = {"list": list(Area.objects.values())}
    return render(request , "admin/Forms/CameraForm.html",context = context)


def CameraLinkForm(request,id):
    cameras = list(Camera.objects.values())
    result = []
    indexMatch = -1
    for i in range(len(cameras)):
        if cameras[i]["id"]==id:
            indexMatch = i
            break
    mainCamera = cameras[indexMatch]
    cameras.pop(indexMatch)
    for i in range(len(cameras)):
        print(cameras[i])
        if cameras[i]["cameraClose_id"] == None or cameras[i]["cameraClose2_id"]== None:
            result.append(cameras[i])
    
    context = {"list": result,"main":mainCamera}
    print(context)
    return render(request , "admin/Forms/CameraLinksForm.html",context = context)