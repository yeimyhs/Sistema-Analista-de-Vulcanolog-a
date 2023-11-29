'''from __future__ import print_function
import gammu
import sys
pip install python-gammu https://pypi.org/project/python-gammu/
'''
from rest_framework.serializers import ModelSerializer
from volcanoApp.models import Alert, Alertconfiguration, Blob, Eventtype, History, Imagesegmentation, Mask, Station, Temporaryseries, Volcano\
, UserP, Mapping, Ashdispersion, Ashfallprediction, Winddirection

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
        imageprofile=validated_data.get('imageprofile', ''),
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
            'imageprofile',
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
        imageprofile=validated_data.get('imageprofile', ''),
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
        'imageprofile',
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

'''
def send_sms_messages(recipients, message_text):
    # Create object for talking with phone
    state_machine = gammu.StateMachine()

    # Optionally load config file as defined by first parameter
    if len(sys.argv) > 1:
        # Read the configuration from given file
        state_machine.ReadConfig(Filename=sys.argv[1])
    else:
        # Read the configuration (~/.gammurc)
        state_machine.ReadConfig()

    # Connect to the phone
    state_machine.Init()

    for recipient in recipients:
        # Prepare message data for each recipient
        message = {
            "Text": message_text,
            "SMSC": {"Location": 1},
            "Number": recipient,
        }

        # Send the message to the current recipient
        state_machine.SendSMS(message)
'''

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
            if self.instance.startalert == 1:
                if self.instance.heighmask > alertconf.altitudalertconf:
                    nueva_alerta = Alert(
                        messagealert=alertconf.messagetemplateconfalert,  # Reemplaza con el mensaje real
                        statealert=1,  # Reemplaza con el estado real
                        idvolcano=idvolcanoimg,  # Reemplaza con el ID del volcán asociado
                        idalertconf= alertconf,  # Reemplaza con el ID de la configuración de alerta asociada
                    )
                    message = alertconf.messagetemplateconfalert
                    if self.instance.mensajeriaalertconf == 1:
                        url = f"https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/sendMessage?chat_id={settings.TELEGRAM_CHANNEL_CHAT_ID}&text={message}"
                        phone_numbers = list(UserP.objects.values_list('phone', flat=True))

                    #print(requests.get(url).json())
                    # Guardar la nueva alerta en la base de datos
                    '''
                    # lista de todos los numeros
                    message = client.mess ages.create(
                        from_='whatsapp:+14155238886',
                        body=alertconf.messagetemplateconfalert,
                        to=['whatsapp:+51973584851']
                        )
                    '''
                    #########send_sms_messages(phone_numbers,alertconf.messagetemplateconfalert)
                    nueva_alerta.save()



'''
class MeteorologicaldataSerializer(ModelSerializer):

    class Meta:
        model = Meteorologicaldata
        fields = '__all__'
'''

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

class WinddirectionSerializer(ModelSerializer):

    class Meta:
        model = Winddirection
        fields = '__all__'

class AshfallpredictionSerializer(ModelSerializer):

    class Meta:
        model = Ashfallprediction
        fields = '__all__'

class AshdispersionSerializer(ModelSerializer):

    class Meta:
        model = Ashdispersion
        fields = '__all__'