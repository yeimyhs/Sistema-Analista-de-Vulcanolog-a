from rest_framework.viewsets import ModelViewSet
from volcanoApp.serializers import AlertSerializer, AlertconfigurationSerializer, BlobSerializer, EventtypeSerializer, HistorySerializer, ImagesegmentationSerializer, MaskSerializer, MeteorologicaldataSerializer, StationSerializer, TemporaryseriesSerializer, VolcanoSerializer \
    , UserPSerializer
from volcanoApp.models import Alert, Alertconfiguration, Blob, Eventtype, History, Imagesegmentation, Mask, Meteorologicaldata, Station, Temporaryseries, Volcano \
    , UserP
from django.contrib.auth.models import User

#----------------------------------------------------------------------Register imports
from .serializers import RegisterSerializer , UserSerializer
from knox.models import AuthToken, User
from rest_framework import generics
from django.db import transaction
from rest_framework.response import Response
#----------------------------------------------------------------------Login imports
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth import login
#----------------------------------------------------------------------swagger imports
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
#https://drf-yasg.readthedocs.io/en/stable/custom_spec.html


#----------------------------------------------------------------------Register

# Register API
class RegisterAPI(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, user_profile = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })
#----------------------------------------------------------------------Login
class LoginAPI(KnoxLoginView):
    
    permission_classes = (permissions.AllowAny,)
    @swagger_auto_schema( request_body=AuthTokenSerializer)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)

#----------------------------------------------------------------------service

      #bytoken

class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = UserPSerializer
    def get_object(self):
        try :
            user = self.request.user
            queryset = UserP.objects.filter(id=user.id).first()
            return queryset
        except:
            return Response({'error': 'No se ha encontrado'})


class AlertViewSet(ModelViewSet):
    queryset = Alert.objects.order_by('pk')
    serializer_class = AlertSerializer


class AlertconfigurationViewSet(ModelViewSet):
    queryset = Alertconfiguration.objects.order_by('pk')
    serializer_class = AlertconfigurationSerializer


class BlobViewSet(ModelViewSet):
    queryset = Blob.objects.order_by('pk')
    serializer_class = BlobSerializer


class EventtypeViewSet(ModelViewSet):
    queryset = Eventtype.objects.order_by('pk')
    serializer_class = EventtypeSerializer


class HistoryViewSet(ModelViewSet):
    queryset = History.objects.order_by('pk')
    serializer_class = HistorySerializer


class ImagesegmentationViewSet(ModelViewSet):
    queryset = Imagesegmentation.objects.order_by('pk')
    serializer_class = ImagesegmentationSerializer


class MaskViewSet(ModelViewSet):
    queryset = Mask.objects.order_by('pk')
    serializer_class = MaskSerializer


class MeteorologicaldataViewSet(ModelViewSet):
    queryset = Meteorologicaldata.objects.order_by('pk')
    serializer_class = MeteorologicaldataSerializer


class StationViewSet(ModelViewSet):
    queryset = Station.objects.order_by('pk')
    serializer_class = StationSerializer


class TemporaryseriesViewSet(ModelViewSet):
    queryset = Temporaryseries.objects.order_by('pk')
    serializer_class = TemporaryseriesSerializer


class UserPViewSet(ModelViewSet):
    queryset = UserP.objects.order_by('pk')
    serializer_class = UserPSerializer


class VolcanoViewSet(ModelViewSet):
    queryset = Volcano.objects.order_by('pk')
    serializer_class = VolcanoSerializer
