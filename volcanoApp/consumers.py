# En tu_app/consumers.py

from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.generic.websocket import WebsocketConsumer

class Tsrealtime(WebsocketConsumer):
    def connect(self):
        self.accept()
    def disconnect(self, close_code):
        pass
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        self.send(text_data=json.dumps({
            'message': message
        }))


from channels.generic.websocket import AsyncWebsocketConsumer
import json

class NotificacionesConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.volcan_id = self.scope['url_route']['kwargs']['volcan_id']
        self.group_name = f"volcan_{self.volcan_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def enviar_mensaje(self, event):
        mensaje = event['contenido']
        await self.send(text_data=json.dumps(mensaje))
