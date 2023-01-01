import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
from survallence.consumers import CameraConsumer
from django.urls import path
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "IS_CHAT.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    # Just HTTP for now. (We can add other protocols later.)
    "websocket": URLRouter([
     path('ws/<groupid>', CameraConsumer.as_asgi())
])
})