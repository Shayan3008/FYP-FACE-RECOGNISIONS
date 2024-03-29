from random import randint
import threading
import time
from models.gait.gait2 import load_model,main
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from cameras.models import Camera

from metaData.models import metadata

class ModelThread(threading.Thread):

    def __init__(self,input,video_name,cameraId):
        self.input = input
        self.video_name = video_name
        self.cameraId = cameraId
        threading.Thread.__init__(self=self)
    
    def run(self):
        reid = load_model()
        video_path = main(reid, self.input, self.video_name)
        
        video_path = video_path[8:-1]
        # temp.save()
        video_path = "test6.mp4" 
        camera1 = Camera.objects.get(id = self.cameraId)
        temp = metadata(camera_id = camera1,video_name = video_path)
        
        time.sleep(10)

        channel_layer = get_channel_layer()
        print("Hello From The Other Thread")
        async_to_sync(channel_layer.group_send)(
            'police',
            {'type': 'update', 'message': 'ALERT CRIME'}
        )
    