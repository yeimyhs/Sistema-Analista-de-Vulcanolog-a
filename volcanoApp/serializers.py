from rest_framework.serializers import ModelSerializer
from volcanoApp.models import Alert, Alertconfiguration, Blob, Eventtype, History, Imagesegmentation, Mask, Meteorologicaldata, Station, Temporaryseries, Volcano\
, UserP

from django.contrib.auth.models import User

from django.db import transaction
#-------------------------------
# User Serializer
@transaction.atomic
def create_user_and_profile(validated_data):
    user = User.objects.create_user(
        validated_data['username'], 
        validated_data['email'], 
        validated_data['password'],
    )

    user_profile = UserP(
        id=user,
        username=user.username,
        email=user.email,
        firstname=validated_data['firstname'],
        lastname=validated_data['lastname'],
        country=validated_data['country'],
        phone=validated_data['phone'],
        adress=validated_data['adress'],
        city=validated_data['city'],
        imagecover=validated_data['imagecover'],
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
        'username', 
        'email' ,
        'imagecover',
        'firstname',
        'lastname',
        'country',
        'phone',
        'adress',
        'city',
        'state',
        'datecreation',
        'type'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user, user_profile = create_user_and_profile(validated_data)
        return user

class RegisterSerializer(ModelSerializer):
    class Meta:
        model = UserP
        fields = [
            'username',
            'email',
            'password',
            'imagecover',
            'firstname',
            'lastname',
            'country',
            'phone',
            'adress',
            'city',
            'type'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
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


class MaskSerializer(ModelSerializer):

    class Meta:
        model = Mask
        fields = '__all__'


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


