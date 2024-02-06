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


from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = self.room_name
        self.room_group_name = f"volcan_{self.room_name}"
        
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

from channels.generic.websocket import WebsocketConsumer
import threading
import time

class CountingWebSocketConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

        # Inicia un hilo para la cuenta infinita
        self.count_thread = threading.Thread(target=self.start_counting)
        self.count_thread.daemon = True  # El hilo terminará cuando el consumidor se desconecte
        self.count_thread.start()

    def disconnect(self, close_code):
        # Detiene el hilo si está corriendo
        if hasattr(self, 'count_thread') and self.count_thread.is_alive():
            self.count_thread.do_run = False  # Marca la bandera para que el hilo termine

    def start_counting(self):
        count = 0
        while getattr(threading.currentThread(), "do_run", True):
            # Realiza la cuenta infinita
            count += 1

            # Envía el resultado a los clientes conectados
            self.send(text_data=str(count))

            # Simula el tiempo entre cuentas
            time.sleep(1)

class notifpush(WebsocketConsumer):
    def connect(self):
        print("---holi")
        
        self.room_group_name = "canal_notif_alert"
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()
        print("---holi")


    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        # Aquí es donde puedes manejar los mensajes entrantes si es necesario
        pass

    def send_notification_to_client(self, event):
        # Método para enviar la notificación al cliente conectado
        message = event["message"]
        self.send(text_data=json.dumps({"message": message}))

    # Método para manejar mensajes enviados desde otra parte de la aplicación
    def send_notification_from_server(self, event):
        message = event["message"]
        # Realizar acciones con el mensaje enviado desde otro lugar de la aplicación
        # Enviar el mensaje de vuelta a los clientes conectados
        self.send(text_data=json.dumps({"message": message}))

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from obspy.clients.earthworm import Client
from obspy import UTCDateTime
import json
from asyncio import sleep
from obspy import Stream, Trace

class realtimeSTobspy(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.cantidad = int(self.scope['url_route']['kwargs']['cantidad']) - 1
        self.segmento = 100 // self.cantidad

        self.earthworm_ip = '10.0.20.55'
        self.earthworm_port = 16025
        self.network = 'PE'
        self.station = 'SAB'
        self.location = ''
        self.channel = 'BH?'

        await self.send_data_in_real_time()

    async def send_data_in_real_time(self):
        while True:
            current_time = UTCDateTime()
            start_time = current_time - 8
            end_time = current_time - 7

            try:
                client = Client(self.earthworm_ip, self.earthworm_port)
                st = client.get_waveforms(self.network, self.station, self.location, self.channel, start_time, end_time)

                if st:
                    trace = st[0]
                    trace.decimate(self.segmento, strict_length=False, no_filter=True)
                    values = trace.data
                    times = trace.times()

                    result = [
                        {"time": str(UTCDateTime(start_time + time)), "value": int(value)} for time, value in zip(times, values)
                    ]

                    for entry in result:
                        await self.send(text_data=json.dumps(entry))
                        print(entry)
                        await sleep(0.00001)

                    print("------------------------")
                    await sleep(1)
                else:
                    await sleep(1)
            except Exception as e:
                print(f"Error: {str(e)}")
                await sleep(1)

    async def disconnect(self, close_code):
        await super().disconnect(code=close_code)
