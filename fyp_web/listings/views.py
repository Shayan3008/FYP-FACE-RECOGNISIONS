from django.shortcuts import render
from area.models import Area
from cameras.models import Camera
from policemans.models import policeman
from shared.Shared_Methods import Shared_Methods
# Create your views here.

def cameraList(request):
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
    return render(request, "admin/List/CameraList.html",context)

def AreaList(request):
    shared = Shared_Methods()
    Table_Head = shared.GetAllColumnNamesFromTable(Area)
    dataList = list(Area.objects.values())
    context = {"list": dataList,"list2":Table_Head}
    return render(request, "admin/List/AreaList.html",context)

def PoliceList(request):
    shared = Shared_Methods()
    Table_Head = shared.GetAllColumnNamesFromTable(policeman)
    Table_Head.reverse()
    Table_Head.pop(Table_Head.index("password"))
    dataList = list(policeman.objects.values("area_id","email","id"))
    context = {"list": dataList,"list2":Table_Head}
    return render(request, "admin/List/SignupList.html",context=context)