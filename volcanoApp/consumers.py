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


from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio
from obspy.clients.earthworm import Client
from obspy import UTCDateTime
import json

class RealTimeDataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.station_id = self.scope['url_route']['kwargs']['station_id']
        self.running = True
        await self.accept()
        asyncio.create_task(self.stream_realtime_data())

    async def disconnect(self, close_code):
        self.running = False

    async def stream_realtime_data(self):
        client = Client("10.0.20.55", 16025)  # Conéctate al cliente ObsPy (ajusta la configuración según sea necesario)
        value = "waveskewnesstempser"  # Reemplaza con el valor deseado

        while self.running:
            try:
                t1 = UTCDateTime() - 60  # Inicio 60 segundos antes del tiempo actual
                t2 = UTCDateTime()  # Tiempo actual
                st = client.get_waveforms("PE", self.station_id, "", "BH?", t1, t2)

                # Procesa los datos de ObsPy, en este caso suponemos un solo trace
                trace = st[0]
                values = trace.data
                times = trace.times()

                # Crea un diccionario con la información que deseas transmitir a través del WebSocket
                data_to_send = [{'starttimetempser': time, 'value': value, 'type': trace.stats.channel} for time, value in zip(times, values)]

                # Envía los datos a través del canal de WebSocket a los clientes conectados
                await self.send(text_data=json.dumps(data_to_send))

                # Espera 1 segundo antes de la próxima actualización (ajusta según sea necesario)
                await asyncio.sleep(1)

            except Exception as e:
                print("Error:", e)
                await asyncio.sleep(5)  # Espera 5 segundos antes de intentar nuevamente en caso de error

# chat/consumers.py
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class notifpush(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]
        self.room_group_name = "_volcan_push_"
        
        print(self.room_group_name)
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))