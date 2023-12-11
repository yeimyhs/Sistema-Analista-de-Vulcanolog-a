# En tu_app/routing.py

from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path, path
from .consumers import *

websocket_urlpatterns = [
        path('ws/chat/', Tsrealtime.as_asgi()),
        # Define tus rutas de WebSocket y los consumidores correspondientes
]
