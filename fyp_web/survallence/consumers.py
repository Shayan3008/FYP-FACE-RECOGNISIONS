from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync


class CameraConsumer(WebsocketConsumer):

    def connect(self):
        self.room_group_name = 'groupid'
        print(self)
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
        self.send(json.dumps({
            "type": "Connection establish",
            "msg": "Congrats"
        }))

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "Alert_Generate",
                "msg": text_data
            }
        )

    def Alert_Generate(self, event):
        message = event["msg"]
        self.send(json.dumps({
            "type": "Alert",
            "msg": message
        }))
        # text_data_json = json.loads(text_data)
