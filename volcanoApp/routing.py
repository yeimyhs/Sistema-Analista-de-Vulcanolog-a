# En tu_app/routing.py

from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path, path
from .consumers import *

websocket_urlpatterns = [
        path('ws/notificaciones/<str:volcan_id>/', NotificacionesConsumer.as_asgi()),
        path('ws/realtime/<str:station_id>/', RealTimeDataConsumer.as_asgi()),
        #re_path(r'ws/notificaciones/$', NotificacionesConsumer.as_asgi()),
        #path('ws/chat/', Tsrealtime.as_asgi()),
        re_path(r"ws/chat/(?P<room_name>\w+)/$", ChatConsumer.as_asgi()),
        # Define tus rutas de WebSocket y los consumidores correspondientes
]
