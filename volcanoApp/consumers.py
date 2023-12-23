# En tu_app/consumers.py

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import WebsocketConsumer

import asyncio
from obspy.clients.earthworm import Client
from obspy import UTCDateTime
import json

from asgiref.sync import async_to_sync


#
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



class notifpush(WebsocketConsumer):
    room_group_name = "volcan_push_"

    def connect(self):
        
        #print(self.room_group_name)
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