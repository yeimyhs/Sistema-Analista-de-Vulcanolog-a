# En tu_app/routing.py

from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path, path
from .consumers import *

websocket_urlpatterns = [
        #path('ws/realtime/<str:station_id>/', RealTimeDataConsumer.as_asgi()),\
        #re_path(r"ws/notifpush/", notifpush.as_asgi()),
        path("ws/notifpush/", notifpush.as_asgi()),
        re_path(r"ws/realtimestobspy/(?P<cantidad>\d+)/$", realtimeSTobspy.as_asgi()),
        re_path(r"ws/chat/(?P<room_name>\w+)/$", ChatConsumer.as_asgi()),

]
