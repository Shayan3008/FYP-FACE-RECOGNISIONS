from django.shortcuts import render

from area.models import Area

# Create your views here.
def AreaForm(request):
    return render(request, "admin/Forms/AreaForm.html")

def PoliceForm(request):
    context = {"list": list(Area.objects.values())}
    return render(request , "admin/Forms/PoliceSignupForm.html",context = context)