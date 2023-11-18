from rest_framework.serializers import ModelSerializer
from volcanoApp.models import Alert, Alertconfiguration, Blob, Eventtype, History, Imagesegmentation, Mask, Meteorologicaldata, Station, Temporaryseries, Volcano\
, UserP, Mapping

from django.contrib.auth.models import User

from django.db import transaction
from rest_framework import serializers
#-------------------------------
from django.contrib.auth.models import User
from rest_framework import serializers
from django.db import transaction
from .models import UserP

from django.conf import settings

from firebase_admin.exceptions import FirebaseError

@transaction.atomic
def create_user_and_profile(validated_data):
    # Extraer 'names' del validated_data
    names = validated_data.pop('names', '')

    # Crear el usuario
    user = User.objects.create_user(
        username=names,  # Usar 'names' como username
        email=validated_data['email'],
        password=validated_data['password'],
    )

    # Crear el perfil de usuario (UserP)
    user_profile = UserP(
        id=user,  # Asignar el usuario recién creado
        names=names,  # Usar 'names' como nombres
        email=user.email,
        lastname=validated_data.get('lastname', ''),
        country=validated_data.get('country', ''),
        city=validated_data.get('city', ''),
        imagecover=validated_data.get('imagecover', ''),
        comment=validated_data['comment'],
    )
    user_profile.save()

    return user, user_profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
        )

    def create(self, validated_data):
        user, user_profile = create_user_and_profile(validated_data)
        return user

class UserPSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserP
        fields = [
            'id',
            'names',
            'lastname',
            'email',
            'institution',
            'country',
            'city',
            'state',
            'datecreation',
            'type',
            'comment',
            'phone'
        ]

# User Serializer
@transaction.atomic
def create_user_and_profile(validated_data):
    # Extraer 'names' del validated_data
    names = validated_data.pop('names', '')

    # Crear el usuario
    user = User.objects.create_user(
        username=names,  # Usar 'names' como username
        email=validated_data['email'],
        password=validated_data['password'],
    )

    # Crear el perfil de usuario (UserP)
    user_profile = UserP(
        id=user,  # Asignar el usuario recién creado
        names=names,  # Usar 'names' como nombres
        email=user.email,
        lastname=validated_data.get('lastname', ''),
        country=validated_data.get('country', ''),
        city=validated_data.get('city', ''),
        imagecover=validated_data.get('imagecover', ''),
        comment=validated_data['comment'],
        phone=validated_data['phone'],
        
    )
    user_profile.save()

    return user, user_profile
class UserSerializer(ModelSerializer):
   # user_profile = UserPSerializer(required=True)
    class Meta:
        model = User
        fields = (
        'id', 
        'username', 
        'email' ,
        
        )
    def create(self, validated_data):
        user, user_profile = create_user_and_profile(validated_data)
        return user


class UserPSerializer(ModelSerializer):
    class Meta:
        model = UserP
        fields = [
        'id',
        'names',
        'lastname',
        'email',
        'institution',
        'country',
        'city',
        'state',
        'datecreation',
        'type',
        'comment',
        'imagecover',
        'phone'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        raise serializers.PermissionDenied("Creation not allowed through this endpoint.")

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserP
        fields = [
            'names',
            'lastname',
            'password',
            'email',
            'institution',
            'comment',
            'phone'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Extrae el valor de 'names'
        user, user_profile = create_user_and_profile(validated_data)
        try:
                userf = auth.create_user(
                    email=user.email,
                    email_verified=False,
                    phone_number=user_profile.phone,
                )
                print (userf.uid)
        except FirebaseError as e:
            print(e)
        return user, user_profile
       
 
 
class AlertSerializer(ModelSerializer):

    class Meta:
        model = Alert
        fields = '__all__'


class AlertconfigurationSerializer(ModelSerializer):

    class Meta:
        model = Alertconfiguration
        fields = '__all__'



class BlobSerializer(ModelSerializer):

    class Meta:
        model = Blob
        fields = '__all__'


class EventtypeSerializer(ModelSerializer):

    class Meta:
        model = Eventtype
        fields = '__all__'


class HistorySerializer(ModelSerializer):

    class Meta:
        model = History
        fields = '__all__'


class ImagesegmentationSerializer(ModelSerializer):

    class Meta:
        model = Imagesegmentation
        fields = '__all__'

import requests
from django.conf import settings
from firebase_admin import auth
from firebase_admin import messaging
#from twilio.rest import Client
#client = Client(settings.TWILIO_WSP_ACCOUNT_SID, settings.TWILIO_WSP_AUTH_TOKEN)
from firebase_admin import messaging

def send_sms_messages(message_text):
    #usuarios_tipo_especifico = UserP.objects.all#UserP.objects.filter(type=tipo_usuario)
    phone_numbers = list(UserP.objects.values_list('phone', flat=True))
    print("-------------", phone_numbers)
    phone_numbers = ["eyJhbGciOiJSUzI1NiIsImtpZCI6IjQ0ZmJkZTdhZGY0ZTU3YWYxZWE4MzAzNmJmZjdkMzUxNTk3ZTMzNWEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vcHJveWVjdG8tc2FiYW5jYXlhIiwiYXVkIjoicHJveWVjdG8tc2FiYW5jYXlhIiwiYXV0aF90aW1lIjoxNzAwMDE4NTc4LCJ1c2VyX2lkIjoiVndSRktUOHZwOVZLRmlqcXJoSmpiaVJNSzZJMyIsInN1YiI6IlZ3UkZLVDh2cDlWS0ZpanFyaEpqYmlSTUs2STMiLCJpYXQiOjE3MDAwMTg1NzgsImV4cCI6MTcwMDAyMjE3OCwiZW1haWwiOiJqdWFuQHRlc3QuY29tIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbImp1YW5AdGVzdC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.JaS8IBu5aYMW2V0TTjxKZCe-6VnHYS2saxOOlRX-E7y5H1DsrwLFibH8s5IX88xE4KfMRjgvjqIxj2VzSxzM5v9Ts76mHof_s6bAFRBLlbzkftKfp9jDbMvWF1h3ogBlm2Aldw-AcLl4mgsY2wCS1Oi0t1_xZ6aCfQuwkG_hg2Pnm3IfMUUKySblzeuERXSaJGY_mzmlCFMAvX-NzPwnF_pMaecfXzmgp8zbC0mZQLq2hpIsqzlzwTO8Czx3Br81lz4WRJ4eIpQlh84ZFah4k1C1kLmjVvckFEKT0HTFfIS2EDNpi_etonqt0MVA-OxcvgYFSjX5VRnokEiKo7u3uw"]
    for phone_number in phone_numbers:
        '''# Verificar si el número de teléfono tiene 9 dígitos (formato peruano)
        if len(phone_number) != 9:
            print(f"Número de teléfono no válido para Perú ({phone_number})")
            continue'''
   
        # Construir el mensaje
        message = messaging.Message(
            data={
                'message': message_text,
            },
            token=phone_number  # Enviar el mensaje al número de teléfono
        )

        # Enviar el mensaje
        try:
            response = messaging.send(message)
            print(f"Mensaje enviado a {phone_number} exitosamente:", response)
        except Exception as e:
            print(f"Error al enviar el mensaje a {phone_number}:", e)

class MaskSerializer(ModelSerializer):

    class Meta:
        model = Mask
        fields = '__all__'
    @transaction.atomic
    def save(self, *args, **kwargs):
        # Realizar el condicional aquí
        super().save(*args, **kwargs)
        volcano_obj= self.instance.idmask.idstation.idvolcano,  # Reemplaza con el ID del volcán asociado
        idvolcanoimg = volcano_obj[0]
        #print("------------------",idvolcanoimg)
        alertconf = Alertconfiguration.objects.filter(idvolcano=idvolcanoimg).first()
        #print("------------------",alertconf)
        if alertconf is not None:
            if self.instance.heighmask > alertconf.altitudalertconf:
                nueva_alerta = Alert(
                    messagealert=alertconf.messagetemplateconfalert,  # Reemplaza con el mensaje real
                    statealert=1,  # Reemplaza con el estado real
                    idvolcano=idvolcanoimg,  # Reemplaza con el ID del volcán asociado
                    idalertconf= alertconf,  # Reemplaza con el ID de la configuración de alerta asociada
                )
                message = alertconf.messagetemplateconfalert
                url = f"https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/sendMessage?chat_id={settings.TELEGRAM_CHANNEL_CHAT_ID}&text={message}"
                #print(requests.get(url).json())
                # Guardar la nueva alerta en la base de datos
                '''
                # lista de todos los numeros
                message = client.messages.create(
                    from_='whatsapp:+14155238886',
                    body=alertconf.messagetemplateconfalert,
                    to=['whatsapp:+51973584851']
                    )
                '''
                #send_sms_messages(alertconf.messagetemplateconfalert)
                nueva_alerta.save()




class MeteorologicaldataSerializer(ModelSerializer):

    class Meta:
        model = Meteorologicaldata
        fields = '__all__'


class StationSerializer(ModelSerializer):

    class Meta:
        model = Station
        fields = '__all__'


class TemporaryseriesSerializer(ModelSerializer):

    class Meta:
        model = Temporaryseries
        fields = '__all__'


class VolcanoSerializer(ModelSerializer):

    class Meta:
        model = Volcano
        fields = '__all__'


class MappingSerializer(ModelSerializer):

    class Meta:
        model = Mapping
        fields = '__all__'