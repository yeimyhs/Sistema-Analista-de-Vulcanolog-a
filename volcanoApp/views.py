from rest_framework.viewsets import ModelViewSet
from volcanoApp.serializers import AlertSerializer, AlertconfigurationSerializer, BlobSerializer, EventtypeSerializer, HistorySerializer, ImagesegmentationSerializer, MaskSerializer, StationSerializer, TemporaryseriesSerializer, VolcanoSerializer \
    , UserPSerializer ,MappingSerializer, AshdispersionSerializer, WinddirectionSerializer, AshfallpredictionSerializer
from volcanoApp.models import Alert, Alertconfiguration, Blob, Eventtype, History, Imagesegmentation, Mask, Station, Temporaryseries, Volcano \
    , UserP, Mapping, Ashdispersion, Ashfallprediction, Winddirection
import volcanoApp.filters  
from django.contrib.auth.models import User
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
#----------------------------------------------------------------------Register imports
from .serializers import RegisterSerializer , UserSerializer
from knox.models import AuthToken, User
from rest_framework import generics
from django.db import transaction
from rest_framework.response import Response

from rest_framework import status
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
 #----------------------------------------------------------------------imports mailer
from django.conf import settings
from rest_framework.response import Response
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.views import APIView

#----------------------------------------------------------------------MaskImgRawPerTime

    #Me parece al tipo de usuario invitado y analista son los permitidos
from datetime import datetime, timedelta
from django.db.models import Q
from rest_framework import generics
from rest_framework.response import Response
from .models import Mask, Imagesegmentation

#----------------------------------------------------------------------password reset imports
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib import messages

from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
#----------------------------------------------------------------------password reset
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
import json
@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_request(request):
    if request.method == "POST":
        try:
            json_data = json.loads(request.body)
            email = json_data.get('email', '')  # Obtener el correo electrónico del payload JSON
        except json.JSONDecodeError:
            return JsonResponse({"error": "Datos JSON inválidos"})

        print(email)
        associated_users = User.objects.filter(Q(email=email))
        print(associated_users)
        if associated_users.exists():
            
            for user in associated_users:
                subject = "Solicitud de restablecimiento de contraseña"
                email_template_name = "password_reset/password_reset_email.html"
                c = {
                "email":user.email,
                'domain':settings.DOMAIN,
                'site_name': 'VolcanoApp',
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "user": user,
                'token': default_token_generator.make_token(user),
                'protocol': 'http',
                }
                email_con = render_to_string(email_template_name, c)
            try:
                send_mail(subject, strip_tags(email_con), settings.EMAIL_HOST_USER, [user.email], html_message=email_con)
                return JsonResponse({"message": "Correo de restablecimiento de contraseña enviado correctamente"})
            except BadHeaderError:
                return JsonResponse({"error": "Envío no realizado"})
        return JsonResponse({"error": "Solicitud inválida"})

    return JsonResponse({"error": "Solicitud inválida"})
#----------------------------------------------------------------------MaskImgRawPerTime

'''class MeteorologicalDataPertTime(generics.GenericAPIView):
    queryset = []  # Define una consulta ficticia

    def get(self, request, idstation, starttime, finishtime,value= "vmet"):
        try:
            idstation = idstation
            starttime = datetime.strptime(starttime, '%Y-%m-%dT%H:%M:%S.%f')
            finishtime = datetime.strptime(finishtime, '%Y-%m-%dT%H:%M:%S.%f')
            #lapsemin = int(lapsemin)
            #starttime = starttime - timedelta(hours=6)
            MDs_within_interval = Meteorologicaldata.objects.filter(statemet=1).filter(
                Q(idstation=idstation),
                starttimemet__gte=starttime,
                starttimemet__lte=finishtime
            )
            serializer = MeteorologicaldataSerializer(MDs_within_interval, many=True)
            response_data = [{'starttime': item['starttimemet'], 'value': item[value]} for item in serializer.data]

            return Response({'results': response_data})
        except Exception as e:
            return Response({'error': str(e)})#----------------------------------------------------------------------MaskImgRawPerTime
'''
from rest_framework.pagination import PageNumberPagination

class TempSeriesPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

from obspy.clients.earthworm import Client
from obspy import UTCDateTime
import time

class TempSeriesPerTime(generics.GenericAPIView):
    queryset = []  # Define una consulta ficticia
    pagination_class = TempSeriesPagination
    def get(self, request, idstation, starttime, finishtime, value='waveskewnesstempser'):
        try:
            #starttime = datetime.strptime(starttime, '%Y-%m-%dT%H:%M:%S.%f')
            #finishtime = datetime.strptime(finishtime, '%Y-%m-%dT%H:%M:%S.%f')
            t1 = UTCDateTime(starttime)
            print("-----------")
            
            t2 = UTCDateTime(finishtime)
        
            print("-----------")
            
            client = Client("10.0.20.55",16025)
            st = client.get_waveforms("PE", idstation, "", "BH?", t1, t2)

            #lapsemin = int(lapsemin)
            #starttime = starttime - timedelta(hours=6)
            '''TSs_within_interval = Temporaryseries.objects.filter(statetempser=1).filter(
                Q(idstation=idstation),
                starttimetempser__gte=starttime,
                starttimetempser__lte=finishtime
            )'''
            
            trace = st[0]  # Suponiendo que st es la lista de traces que obtuviste de ObsPy
            print('-',trace)
            # Accede a los valores de la serie temporal y los tiempos correspondientes
            values = trace.data
            times = trace.times()

            # Genera una lista de diccionarios con la información requerida
            response_data = [{'starttimetempser': time, 'value': value, 'type': trace.stats.channel} for time, value in zip(times, values)]


            #serializer = TemporaryseriesSerializer(TSs_within_interval, many=True)
            #response_data = [{'starttimetempser': item['starttimetempser'], 'value': item[value], 'type' : item['ideventtype']} for item in serializer.data]
            
            paginated_response = self.paginate_queryset(response_data)
            if paginated_response is not None:
                return self.get_paginated_response(paginated_response)
            
            return Response({'results': response_data})
        
        except Exception as e:
            return Response({'error': str(e)})
#----------------------------------------------------------------------MaskImgRawPerTime
class BlobsStationperMask(generics.GenericAPIView):
    queryset = []  # Define una consulta ficticia

    def get(self, request, idmask):
      
            mask= Mask.objects.get(idmask = idmask)
            blobs = Blob.objects.filter(stateblob=1).filter(idmask=idmask)
            results = []
            results.append({
                'Station': StationSerializer(mask.idstation).data,
                'Blobs': BlobSerializer(blobs, many=True).data,
            })
            return Response({'results': results})
     
#----------------------------------------------------------------------MaskImgRawPerTime

class MaskImgRawPerTime(generics.GenericAPIView):
    queryset = []  # Define una consulta ficticia

    def get(self, request, idstation, starttime, finishtime):
        try:
            idstation = idstation
            starttime = datetime.strptime(starttime, '%Y-%m-%dT%H:%M:%S.%f')
            finishtime = datetime.strptime(finishtime, '%Y-%m-%dT%H:%M:%S.%f')
            #lapsemin = int(lapsemin)
            #starttime = starttime - timedelta(hours=6)
            masks_within_interval = Mask.objects.filter(statemask=1).filter(
                Q(idmask__idstation=idstation),
                starttimemask__gte=starttime,
                starttimemask__lte=finishtime
            )
            results = []
            for mask in masks_within_interval:
                segmentation_image = Imagesegmentation.objects.filter(stateimg=1).get(idphoto=mask.idmask.idphoto)
                results.append({
                    'mask': MaskSerializer(mask).data,
                    'segmentation_image': ImagesegmentationSerializer(segmentation_image).data
                })
            return Response({'results': results})
        except Exception as e:
            return Response({'error': str(e)})
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
        "token": AuthToken.objects.create(user)[1]
        })
#----------------------------------------------------------------------Login
from knox.views import LoginView as KnoxLoginView
from rest_framework.response import Response

class LoginAPI(KnoxLoginView):
    
    permission_classes = (permissions.AllowAny,)
    @swagger_auto_schema( request_body=AuthTokenSerializer)

    def post(self, request, format=None):
        print(request.data)
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'error': 'Credenciales inválidas.'}, status=400)
        datas= {'username': user.username, 'password': password}
        serializer = AuthTokenSerializer(data=datas)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)

#----------------------------------------------------------------------service

      #bytokenzs

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

#----------------------------------------------------------------------Paginacion
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    page_size_query_param = 'page_size'  # Parámetro para especificar la cantidad de elementos por página
    #max_page_size = 100
    
    def get_paginated_response(self, data):
        page_size = self.request.query_params.get(self.page_size_query_param)
        #print("Valor de 'page_size' en CustomPagination:", page_size)
        if page_size == "none":
            page_size = None
            print("----------------")
        print("Valor de 'page_size' en CustomPagination:", page_size)
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'page_size': page_size,
            'results': data
        })

 #----------------------------------------------------------------------mailer

class mailer(APIView):
    permission_classes = [permissions.AllowAny, ]
    def post(self,request):
        subject= request.data["subject"]
        message= request.data["message"] + " " + request.data["email"]
        from_email= settings.EMAIL_HOST_USER
        recipient_list= settings.EMAIL_HOST_USER
        '''{
        "subject":"subject",
        "message":"message",
        "email":"email"
        }'''
        if subject and message and from_email:
            try:
                send_mail(subject, message, from_email, [recipient_list])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            #return HttpResponseRedirect('/contact/thanks/')
            return HttpResponse('The email was send.')
        else:
            return HttpResponse('Make sure all fields are entered and valid.',request.data)
 #----------------------------------------------------------------------

class AlertViewSet(ModelViewSet):
    queryset = Alert.objects.filter(statealert=1).order_by('pk')
    serializer_class = AlertSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter,filters.SearchFilter]
    filterset_class = volcanoApp.filters.AlertFilter
    search_fields = ['idalert',
                  'idvolcano__longnamevol',
                  'idvolcano__shortnamevol', 
                  'idvolcano__descriptionvol' ,
                     'messagealert'
                  ] 

'''    pagination_class = CustomPagination 

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
'''

class AlertconfigurationViewSet(ModelViewSet):
    queryset = Alertconfiguration.objects.filter(statealertconf=1).order_by('pk')
    serializer_class = AlertconfigurationSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter,filters.SearchFilter]
    filterset_class = volcanoApp.filters.AlertConfFilter 
    search_fields = ['idalertconf', 
                  'idvolcano__longnamevol',
                  'notificationalertconf', 
                  'messagetemplateconfalert',
                  'idvolcano__longnamevol',
                  'idvolcano__shortnamevol', 
                  'idvolcano__descriptionvol']

    
    def all(self, request):
        queryset = Alertconfiguration.objects.all()
        data = AlertconfigurationSerializer(queryset, many=True, context={'request': self.request}).data
        return Response(data)

class BlobViewSet(ModelViewSet):
    queryset = Blob.objects.filter(stateblob=1).order_by('pk')
    serializer_class = BlobSerializer


class EventtypeViewSet(ModelViewSet):
    queryset = Eventtype.objects.filter(stateevent=1).order_by('pk')
    serializer_class = EventtypeSerializer


class HistoryViewSet(ModelViewSet):
    queryset = History.objects.filter(statehistory=1).order_by('pk')
    serializer_class = HistorySerializer


class ImagesegmentationViewSet(ModelViewSet):
    queryset = Imagesegmentation.objects.filter(stateimg=1).order_by('pk')
    serializer_class = ImagesegmentationSerializer


class MaskViewSet(ModelViewSet):
    queryset = Mask.objects.filter(statemask=1).order_by('pk')
    serializer_class = MaskSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter,filters.SearchFilter]
    #pagination_class = None

class AshdispersionViewSet(ModelViewSet):
    queryset = Ashdispersion.objects.filter(stateashdisp=1).order_by('pk')
    serializer_class = AshdispersionSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter,filters.SearchFilter]

class AshfallpredictionViewSet(ModelViewSet):
    queryset = Ashfallprediction.objects.filter(stateashfall=1).order_by('pk')
    serializer_class = AshfallpredictionSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter,filters.SearchFilter]

class WinddirectionViewSet(ModelViewSet):
    queryset = Winddirection.objects.filter(statewinddir=1).order_by('pk')
    serializer_class = WinddirectionSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter,filters.SearchFilter]


class StationViewSet(ModelViewSet):
    queryset = Station.objects.filter(statestat=1).order_by('pk')
    serializer_class = StationSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter,filters.SearchFilter]
    filterset_class = volcanoApp.filters.StationFilter 
    search_fields = ['idstation',
                     'standardnamestat',
                     'shortnamestat',
                     'longnamestat',
                     'latitudestat',
                     'longitudestat',
                     'altitudestat',
                     'idvolcano__longnamevol',
                     'typestat']
    def all(self, request):
        queryset = Station.objects.filter(statestat=1)
        data = StationSerializer(queryset, many=True).data
        return Response(data)
    
class TemporaryseriesViewSet(ModelViewSet):
    queryset = Temporaryseries.objects.filter(statetempser=1).order_by('pk')
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter,filters.SearchFilter]
    serializer_class = TemporaryseriesSerializer
class MappingViewSet(ModelViewSet):
    queryset = Mapping.objects.order_by('pk')
    serializer_class = MappingSerializer


class UserPViewSet(ModelViewSet):
    queryset = UserP.objects.filter(state=1).order_by('pk')
    serializer_class = UserPSerializer
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter,filters.SearchFilter]
    filterset_class = volcanoApp.filters.UserPFilter 

    def all(self, request):
        queryset = UserP.objects.filter(state=1)
        data = UserPSerializer(queryset, many=True).data
        return Response(data)


    search_fields = [
        'names',
        'lastname',
        'email',
        'institution',
        'country',
        'city',
        'state',
        'datecreation',
        'type',
        ]
    filterset_fields = [
        'names',
        'lastname',
        'email',
        'institution',
        'country',
        'city',
        'state',
        'datecreation',
        'type',
        ]
    ordering_fields = '__all__'
    def create(self, request, *args, **kwargs):
        # Devuelve una respuesta de error con código 403 (Forbidden)
        return Response({"detail": "La creación de instancias está prohibida en esta vista use el Registro."},
                        status=status.HTTP_403_FORBIDDEN)

class VolcanoViewSet(ModelViewSet):
    queryset = Volcano.objects.filter(statevol=1).order_by('pk')
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter,filters.SearchFilter]
    serializer_class = VolcanoSerializer
    filterset_class = volcanoApp.filters.VolcanoFilter    
    search_fields = ['shortnamevol', 
                  'longnamevol', 
                  'descriptionvol', 
                  'altitudevol', 
                  'pwavespeedvol', 
                  'densityvol', 
                  'attcorrectfactorvol']


    def all(self, request):
        queryset = Volcano.objects.filter(statevol=1)
        data = VolcanoSerializer(queryset, many=True).data
        return Response(data)
    
from django.shortcuts import render

def index(request):
    return render(request, 'websocket/index.html')