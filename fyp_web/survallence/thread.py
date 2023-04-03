import threading
import time
# from models.gait.gait import load_model,main
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class ModelThread(threading.Thread):

    def __init__(self,input,video_name):
        self.input = input
        self.video_name = video_name
        threading.Thread.__init__(self=self)
    
    def run(self):
        # reid = load_model()
        # video_path = main(reid, self.input, self.video_name)
        time.sleep(10)
        channel_layer = get_channel_layer()
        print("Hello From The Other Thread")
        async_to_sync(channel_layer.group_send)(
            'police',
            {'type': 'update', 'message': 'hello from the background thread'}
        )
    