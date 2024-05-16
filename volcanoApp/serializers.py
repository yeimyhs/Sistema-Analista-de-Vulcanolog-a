'''from __future__ import print_function
import gammu
import sys
pip install python-gammu https://pypi.org/project/python-gammu/
'''
from rest_framework.serializers import ModelSerializer
import json
from volcanoApp.models import Alert, Alertconfiguration, Blob, Eventtype, History, Imagesegmentation, Mask, Station, Temporaryseries, Volcano\
, UserP, Mapping, Ashdispersion, Ashfallprediction, Winddirection, Explosion, Alarm

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
       
 
class VolcanoSerializer(ModelSerializer):

    class Meta:
        model = Volcano
        fields = '__all__'

class AlertPushSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = '__all__'
 

class AshdispersionSerializer(ModelSerializer):

    class Meta:
        model = Ashdispersion
        fields = '__all__'


class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if self.context['request'].method in ['GET', 'LIST']:
            # Obtener los detalles de Volcano y añadirlos a la representación
            volcano_details = instance.idvolcano
            representation['volcano_details'] = VolcanoSerializer(volcano_details).data
            idImgRaw_details = instance.idimgraw
            representation['idImgRaw_details'] = ImagesegmentationSerializer(idImgRaw_details).data
            ash_dispersion_details = instance.idashdispersion
            representation['ash_dispersion_details'] = AshdispersionSerializer(ash_dispersion_details).data

        return representation

class AlertconfigurationSerializer(ModelSerializer):

    class Meta:
        model = Alertconfiguration
        fields = '__all__'
    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if self.context['request'].method in ['GET', 'LIST']:
            # Obtener los detalles de Volcano y añadirlos a la representación
            volcano_details = instance.idvolcano
            representation['volcano_details'] = VolcanoSerializer(volcano_details).data

        return representation


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

'''    @transaction.atomic
    def save(self, *args, **kwargs):
        # Realizar el condicional aquí
        super().save(*args, **kwargs)
        volcano_obj= self.instance.idmask.idstation.idvolcano,  # Reemplaza con el ID del volcán asociado
        idvolcanoimg = volcano_obj[0]
        #print("------------------",idvolcanoimg)
        alertconf = Alertconfiguration.objects.filter(idvolcano=idvolcanoimg).first()
        #print("------------------",alertconf)
        if alertconf is not None:
            if alertconf.startalert == 1:
                if self.instance.heighmask > alertconf.altitudalertconf:
                    nueva_alerta = Alert(
                        messagealert=alertconf.messagetemplateconfalert,  # Reemplaza con el mensaje real
                        statealert=1,  # Reemplaza con el estado real
                        idvolcano=idvolcanoimg,  # Reemplaza con el ID del volcán asociado
                        idalertconf= alertconf,  # Reemplaza con el ID de la configuración de alerta asociada
                        heighalert= self.instance.heighmask,
                        idstation= self.instance.idstation,
                        alertlevelalert = self.instance.idmask.idstation.idvolcano.alertlevelvol

                    )
                    message = alertconf.messagetemplateconfalert
                    if alertconf.mensajeriaalertconf == 1:
                        url = f"https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/sendMessage?chat_id={settings.TELEGRAM_CHANNEL_CHAT_ID}&text={message}"
                        phone_numbers = list(UserP.objects.values_list('phone', flat=True))

                    #print(
                        requests.get(url).json()#)
                    # Guardar la nueva alerta en la base de datos
                    # '/''
                    # lista de todos los numeros
                    message = client.mess ages.create(
                        from_='whatsapp:+14155238886',
                        body=alertconf.messagetemplateconfalert,
                        to=['whatsapp:+51973584851']
                        )
                    #''/'
                    #########send_sms_messages(phone_numbers,alertconf.messagetemplateconfalert)
                    nueva_alerta.save()'''



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


from django.core.exceptions import ObjectDoesNotExist


from rest_framework.serializers import ModelSerializer

class ReadOnlyExplosionSerializer(ModelSerializer):
    class Meta:
        model = Explosion
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        image_segmentation = instance.idimage
            # Obtener los detalles de los modelos relacionados y agregarlos a la representación
        try:
                if image_segmentation is not None:
                    # Obtener los detalles de la imagen
                    idimage_details = instance.idimage
                    representation['idimage_details'] = ImagesegmentationSerializer(idimage_details).data
        except ObjectDoesNotExist:
            representation['idimage_details'] = None
            
        try:
            if image_segmentation is not None:
                mask_details = Mask.objects.get(idmask=image_segmentation)
                representation['mask_details'] = MaskSerializer(mask_details).data
        except ObjectDoesNotExist:
            representation['mask_details'] = None

        try:
            idwinddir_details = instance.idwinddir
            if idwinddir_details:
                representation['idwinddir_details'] = WinddirectionSerializer(idwinddir_details).data
        except ObjectDoesNotExist:
            representation['idwinddir_details'] = None
        
        try:
            idashdispersion_details = instance.idashdispersion
            if idashdispersion_details:
                representation['idashdispersion_details'] = AshdispersionSerializer(idashdispersion_details).data
        except ObjectDoesNotExist:
            representation['idashdispersion_details'] = None
        
        try:
            idashfallprediction_details = instance.idashfallprediction
            if idashfallprediction_details:
                representation['idashfallprediction_details'] = AshfallpredictionSerializer(idashfallprediction_details).data
        except ObjectDoesNotExist:
            representation['idashfallprediction_details'] = None
        
        try:
            idvolcano_details = instance.idvolcano
            if idvolcano_details:
                representation['idvolcano_details'] = VolcanoSerializer(idvolcano_details).data
        except ObjectDoesNotExist:
            representation['idvolcano_details'] = None
        
        try:
            idstation_details = instance.idstation
            if idstation_details:
                representation['idstation_details'] = StationSerializer(idstation_details).data
        except ObjectDoesNotExist:
            representation['idstation_details'] = None

        
        return representation

class ExplosionwithoutdetaiilsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Explosion
        fields = '__all__'


class Explosionmask_imagedetaiilsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Explosion
        fields = ['idexplosion', 'starttime', 'ideventtype', 'idimage', 'height', 'detectionmode', 'idstation', 'data']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        image_segmentation = instance.idimage

        # Obtener los detalles de la imagen si está presente
        try:
                if image_segmentation is not None:
                    # Obtener los detalles de la imagen
                    idimage_details = instance.idimage
                    representation['idimage_details'] = ImagesegmentationSerializer(idimage_details).data
        except ObjectDoesNotExist:
            representation['idimage_details'] = None
            

        # Obtener los detalles de la máscara si está presente
        if image_segmentation:
            try:
                mask_details = Mask.objects.get(idmask=image_segmentation)
                representation['mask_details'] = MaskSerializer(mask_details).data
            except Mask.DoesNotExist:
                representation['mask_details'] = None

        # Obtener los detalles de las estaciones desde los datos planos
        data = representation.get('data')
        image = data.get('image', [])
        if data:
            station_details = {}
            for index, station_id in enumerate(data.get('station', [])):
                station_data = {
                    'station_details': station_id,
                    'idimage_details': self.get_imagesegmentation_details(station_id),
                    'mask_details': self.get_mask_details(station_id)
                }
                station_details[image[index]] = station_data

            representation['data']['station_details'] = station_details

        return representation

    def get_imagesegmentation_details(self, idimage):
        try:
            return ImagesegmentationSerializer(Imagesegmentation.objects.get(idphoto=idimage)).data
        except Imagesegmentation.DoesNotExist:
            return None

    def get_mask_details(self, idmask):
        try:
            return MaskSerializer(Mask.objects.get(idmask=idmask)).data
        except Mask.DoesNotExist:
            return None


class ExplosionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Explosion
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if self.context['request'].method in ['GET', 'LIST']:
            image_segmentation = instance.idimage
            # Obtener los detalles de los modelos relacionados y agregarlos a la representación
            try:
                    if image_segmentation is not None:
                        # Obtener los detalles de la imagen
                        idimage_details = instance.idimage
                        representation['idimage_details'] = ImagesegmentationSerializer(idimage_details).data
            except ObjectDoesNotExist:
                representation['idimage_details'] = None
                
            try:
                if image_segmentation is not None:
                    mask_details = Mask.objects.get(idmask=image_segmentation)
                    representation['mask_details'] = MaskSerializer(mask_details).data
            except ObjectDoesNotExist:
                representation['mask_details'] = None

            try:
                idwinddir_details = instance.idwinddir
                if idwinddir_details:
                    representation['idwinddir_details'] = WinddirectionSerializer(idwinddir_details).data
            except ObjectDoesNotExist:
                representation['idwinddir_details'] = None
            
            try:
                idashdispersion_details = instance.idashdispersion
                if idashdispersion_details:
                    representation['idashdispersion_details'] = AshdispersionSerializer(idashdispersion_details).data
            except ObjectDoesNotExist:
                representation['idashdispersion_details'] = None
            
            try:
                idashfallprediction_details = instance.idashfallprediction
                if idashfallprediction_details:
                    representation['idashfallprediction_details'] = AshfallpredictionSerializer(idashfallprediction_details).data
            except ObjectDoesNotExist:
                representation['idashfallprediction_details'] = None
            
            try:
                idvolcano_details = instance.idvolcano
                if idvolcano_details:
                    representation['idvolcano_details'] = VolcanoSerializer(idvolcano_details).data
            except ObjectDoesNotExist:
                representation['idvolcano_details'] = None
            
            try:
                idstation_details = instance.idstation
                if idstation_details:
                    representation['idstation_details'] = StationSerializer(idstation_details).data
            except ObjectDoesNotExist:
                representation['idstation_details'] = None

        return representation
class AlarmSerializer(ModelSerializer):
    # Define un campo para representar los detalles de la idexplosion
    #idexplosion_details = ExplosionSerializer(source='idexplosion', read_only=True)

    class Meta:
        model = Alarm
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if self.context['request'].method in ['GET', 'LIST']:
            # Obtener los detalles de los modelos relacionados y agregarlos a la representación
            try:
                if instance.idexplosion is not None:
                    idexplosion_details = instance.idexplosion
                    representation['idexplosion_details'] = Explosionmask_imagedetaiilsSerializer(idexplosion_details).data
            except ObjectDoesNotExist:
                representation['idexplosion_details'] = None


            try:
                if instance.idvolcano is not None:
                    volcano_details = instance.idvolcano
                    representation['volcano_details'] = VolcanoSerializer(volcano_details).data
            except ObjectDoesNotExist:
                representation['volcano_details'] = None

          

        return representation
    
class AlarmPushSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alarm
        fields = '__all__'