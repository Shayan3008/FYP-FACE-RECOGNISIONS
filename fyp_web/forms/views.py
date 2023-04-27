from django.shortcuts import render

from area.models import Area
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