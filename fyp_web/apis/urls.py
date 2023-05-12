"""fyp_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from apis import views

urlpatterns = [
    path("coordinates/", view=views.getLocationWithCameraId, name="Get Coordinates"),
    path("SendVideo/", view=views.SendVideo,name = "Download Video"),
    path("CheckData/",view=views.GetData,name="Check Data"),
    path("AddCamera/",view = views.AddCamera, name = "Add Camera"),
    path("UserSignup/", view=views.UserSignUp,name="user Signup"),
    path("DeleteData/",view=views.DeleteData,name = "Delete Data",),
    path("UserLogin/",view=views.UserLogin,name="Login User"),
    path("AddPolice/",view=views.AddPoliceman,name = "Adding Policeman"),
    path("AddCameraLinks/",view = views.AddCameraLinks, name = "Add Links"),
    path("PoliceLogin/",view=views.PoliceLogin,name="Police Login"),
    path("GetCookie/" ,view = views.GetCookie, name="Get Cookie"),
    path("AddArea/",view=views.AddArea,name="Add Area"),
    path("GetCameraById/<int:id>",view=views.GetCameraById,name = "Get Camera By Id"),
    path("SendMail/",view=views.ForgotPass,name = "Forgot Pass"),
    path("ChangePass/",view=views.ChangePass,name = "Change Pass")
]

# http://127.0.0.1:8000/apis/SendVideo/