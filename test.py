from obspy.clients.seedlink import Client
from obspy import UTCDateTime
import time

# Crear el cliente SeedLink con los detalles del servidor
server_ip = '10.0.20.55'
server_port = 16025
network = 'PE'
station = 'SAB'
location = ''
channel = 'BH?'

# Conectar al servidor SeedLink
client = Client(server=server_ip, port=server_port)

while True:
    try:
        now = UTCDateTime.now()
        stream = client.get_waveforms(network=network, station=station, location=location, channel=channel, starttime=now - 60, endtime=now)
        
        # Manejar los datos recibidos aquí, por ejemplo:
        for trace in stream:
            print(trace)
        
    except Exception as e:
        print("Error:", e)
    
    # Esperar antes de la próxima actualización de datos
    time.sleep(60)





