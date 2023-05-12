# A class which is used to keep all the shared procedures between the classes

import json
from django.http import HttpRequest
from django.core.serializers.json import DjangoJSONEncoder

class Shared_Methods:
    def __init__(self) -> None:
        pass
    # function to Save file sent from HTTP. Can Be used for both image and video inputs\
    #inputs name: path of the file , file = file sent over Http
    def HandleUploadFile(self,name, file):  
        with open(name + file.name, "wb+") as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        return name+file.name
    # function used as helper to take data from a model and convert it into a list of json
    # input: Model => Object Model whose data is required.
    def SendModelDataApiHelper(self,Model):
        return json.dumps(list(Model.objects.values()),cls = DjangoJSONEncoder)
    
    # function used as helper to delete rows from model.
    # input: Model => Object Model whose data is required.

    def DeleteModelDataApiHelper(self,Model):
        Model.objects.all().delete()
        return "Model Deleted!!!"
    
    def GetAllColumnNamesFromTable(self,Model):
        return [f.get_attname() for f in Model._meta.fields]
