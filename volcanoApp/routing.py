# En tu_app/routing.py

from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path, path
from .consumers import *

websocket_urlpatterns = [
        re_path(r'ws/notificaciones/(?P<volcan_id>\d+)/$', NotificacionesConsumer.as_asgi()),

        #re_path(r'ws/notificaciones/$', NotificacionesConsumer.as_asgi()),
        path('ws/chat/', Tsrealtime.as_asgi()),
        # Define tus rutas de WebSocket y los consumidores correspondientes
]
