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
    """
    Sericio de  solicitud de cambio de contrasenia
    """
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

class WinddirectionPertTime(generics.GenericAPIView):
    """
    Sericio que recopila Direccion de Viento, respondiendo a un intervalo de tiempo con un formato especifico
    """
    queryset = []  # Define una consulta ficticia

    def get(self, request, idvolcano, starttime, finishtime,value= "vwinddir"):
        try:
            starttime = datetime.strptime(starttime, '%Y-%m-%dT%H:%M:%S.%f')
            finishtime = datetime.strptime(finishtime, '%Y-%m-%dT%H:%M:%S.%f')
            #lapsemin = int(lapsemin)
            #starttime = starttime - timedelta(hours=6)
            WDs_within_interval = Winddirection.objects.filter(
                Q(idvolcano=idvolcano),
                starttimewinddir__gte=starttime,
                starttimewinddir__lte=finishtime
            )
            serializer = WinddirectionSerializer(WDs_within_interval, many=True)
            response_data = [{'starttime': item['starttimewinddir'], 'value': item[value]} for item in serializer.data]

            return Response({'results': response_data})
        except Exception as e:
            return Response({'error': str(e)})#----------------------------------------------------------------------MaskImgRawPerTime


class WinddirectionCompletePertTime(generics.ListAPIView):
    """
    Servicio que recopila Dirección de Viento con detalles completos, respondiendo a un intervalo de tiempo con un formato especifico
    """
    queryset = Winddirection.objects.all()
    serializer_class = WinddirectionSerializer
    pagination_class = PageNumberPagination
    pagination_class.page_size = 10
    filter_backends = [filters.OrderingFilter]
    ordering_fields = '__all__'  # Campos por los que se puede ordenar
    
    def get_queryset(self):
        idvolcano = self.kwargs['idvolcano']
        starttime = datetime.strptime(self.kwargs['starttime'], '%Y-%m-%dT%H:%M:%S.%f')
        finishtime = datetime.strptime(self.kwargs['finishtime'], '%Y-%m-%dT%H:%M:%S.%f')

        queryset = self.queryset.filter(
            Q(idvolcano=idvolcano),
            starttimewinddir__gte=starttime,
            starttimewinddir__lte=finishtime
        )
        return queryset.order_by(self.request.query_params.get('ordering', 'starttimewinddir'))


class AshfallpredictionCompletePertTime(generics.ListAPIView):
    """
    Servicio que recopila Predicciones de caída de Ceniza con detalles completos, respondiendo a un intervalo de tiempo con un formato específico
    """
    queryset = Ashfallprediction.objects.all()
    serializer_class = AshfallpredictionSerializer
    pagination_class = PageNumberPagination
    pagination_class.page_size = 10
    filter_backends = [filters.OrderingFilter]
    ordering_fields = '__all__'  # Campos por los que se puede ordenar

    def get_queryset(self):
        idvolcano = self.kwargs['idvolcano']
        starttime = datetime.strptime(self.kwargs['starttime'], '%Y-%m-%dT%H:%M:%S.%f')
        finishtime = datetime.strptime(self.kwargs['finishtime'], '%Y-%m-%dT%H:%M:%S.%f')

        queryset = self.queryset.filter(
            Q(idvolcano=idvolcano),
            starttimeashfall__gte=starttime,
            starttimeashfall__lte=finishtime
        )
        return queryset.order_by(self.request.query_params.get('ordering', 'starttimeashfall'))

class AshfallpredictionPertTime(generics.GenericAPIView):
    """
    Sericio que recopila Predicciones de caida de Ceniza respondiendo a un intervalo de tiempo con un formato especifico
    """
    queryset = []  # Define una consulta ficticia
    def get(self, request, idvolcano, starttime, finishtime,value= "jsonbodyashfall"):
        try:
            starttime = datetime.strptime(starttime, '%Y-%m-%dT%H:%M:%S.%f')
            finishtime = datetime.strptime(finishtime, '%Y-%m-%dT%H:%M:%S.%f')
            #lapsemin = int(lapsemin)
            #starttime = starttime - timedelta(hours=6)
            WDs_within_interval = Ashfallprediction.objects.filter(
                Q(idvolcano=idvolcano),
                starttimeashfall__gte=starttime,
                starttimeashfall__lte=finishtime
            )
            serializer = AshfallpredictionSerializer(WDs_within_interval, many=True)
            response_data = [{'starttime': item['starttimeashfall'], 'value': item[value]} for item in serializer.data]
            return Response({'results': response_data})
        except Exception as e:
            return Response({'error': str(e)})#----------------------------------------------------------------------MaskImgRawPerTime

class AshdispersionPertTime(generics.GenericAPIView):
    """
    Sericio que recopila Dispersion de Ceniza respondiendo a un intervalo de tiempo con un formato especifico
    """
    queryset = []  # Define una consulta ficticia

    def get(self, request, idvolcano, starttime, finishtime,value= "jsonashdisp"):
        try:
            starttime = datetime.strptime(starttime, '%Y-%m-%dT%H:%M:%S.%f')
            finishtime = datetime.strptime(finishtime, '%Y-%m-%dT%H:%M:%S.%f')
            #lapsemin = int(lapsemin)
            #starttime = starttime - timedelta(hours=6)
            #noticeash= Ashdispersion.objects.order_by('starttimeashdisp').first().idnoticeashdisp

            ADs_within_interval = Ashdispersion.objects.filter(
                Q(idvolcano=idvolcano),
                starttimeashdisp__gte=starttime,
                starttimeashdisp__lte=finishtime
            ).order_by('starttimeashdisp')
            serializer = AshdispersionSerializer(ADs_within_interval, many=True)
            response_data = [{'starttime': item['starttimeashdisp'], 'value': item[value], 'idnoticeashdisp':item['idnoticeashdisp'], 'idtypeashdisp':item['idtypeashdisp'] } for item in serializer.data]

            return Response({'results': response_data})
        except Exception as e:
            return Response({'error': str(e)})#----------------------------------------------------------------------MaskImgRawPerTime
        
class AshdispersionidNoticePertTime(generics.GenericAPIView):
    """
    Sericio que recopila Dispercion de Ceniza en base al idNotice y respondiendo a un intervalo de tiempo con un formato especifico
    """
    queryset = []  # Define una consulta ficticia

    def get(self, request, idvolcano, starttime, finishtime,idnoticept1, idnoticept2 ,value= "jsonashdisp"):
        try:
            concatenated_idnotice = f"{idnoticept1}/{idnoticept2}"
            starttime = datetime.strptime(starttime, '%Y-%m-%dT%H:%M:%S.%f')
            finishtime = datetime.strptime(finishtime, '%Y-%m-%dT%H:%M:%S.%f')
            #lapsemin = int(lapsemin)
            #starttime = starttime - timedelta(hours=6)
            ADs_within_interval = Ashdispersion.objects.filter(
                Q(idvolcano=idvolcano),Q(idnoticeashdisp=concatenated_idnotice),
                starttimeashdisp__gte=starttime,
                starttimeashdisp__lte=finishtime
            ).order_by('starttimeashdisp')
            serializer = AshdispersionSerializer(ADs_within_interval, many=True)
            response_data = [{'starttime': item['starttimeashdisp'], 'value': item[value], 'idnoticeashdisp':item['idnoticeashdisp'], 'idtypeashdisp':item['idtypeashdisp'] } for item in serializer.data]

            return Response({'results': response_data})
        except Exception as e:
            return Response({'error': str(e)})#----------------------------------------------------------------------MaskImgRawPerTime
class AshdispersionCompletePertTime(generics.GenericAPIView):
    """
    Sericio que recopila Dispercion de Ceniza con detalls completos ,respondiendo a un intervalo de tiempo con un formato especifico
    """
    queryset = []  # Define una consulta ficticia
    pagination_class = PageNumberPagination
    pagination_class.page_size = 1
    
    def get(self, request, idvolcano, starttime, finishtime,value= "jsonashdisp"):
        try:
            starttime = datetime.strptime(starttime, '%Y-%m-%dT%H:%M:%S.%f')
            finishtime = datetime.strptime(finishtime, '%Y-%m-%dT%H:%M:%S.%f')
            #lapsemin = int(lapsemin)
            #starttime = starttime - timedelta(hours=6)
            #noticeash= Ashdispersion.objects.order_by('starttimeashdisp').first().idnoticeashdisp

            ADs_within_interval = Ashdispersion.objects.filter(
                Q(idvolcano=idvolcano),
                starttimeashdisp__gte=starttime,
                starttimeashdisp__lte=finishtime
            ).order_by('starttimeashdisp')
            paginated_queryset = self.paginate_queryset(ADs_within_interval)
            
            serializer = AshdispersionSerializer(paginated_queryset, many=True)
            #response_data = [{'starttime': item['starttimeashdisp'], 'value': item[value]} for item in serializer.data]

            return self.get_paginated_response(serializer.data) 
        except Exception as e:
            return Response({'error': str(e)})#----------------------------------------------------------------------MaskImgRawPerTime

class TempSeriesPerTime(generics.GenericAPIView):
    """
    Sericio que recopila Series Temporales locales ,respondiendo a un intervalo de tiempo con un formato especifico
    """
    queryset = []  # Define una consulta ficticia

    def get(self, request, idstation, starttime, finishtime, value='waveskewnesstempser'):
        try:
            idstation = idstation
            starttime = datetime.strptime(starttime, '%Y-%m-%dT%H:%M:%S.%f')
            finishtime = datetime.strptime(finishtime, '%Y-%m-%dT%H:%M:%S.%f')
            #lapsemin = int(lapsemin)
            #starttime = starttime - timedelta(hours=6)
            TSs_within_interval = Temporaryseries.objects.filter(statetempser=1).filter(
                Q(idstation=idstation),
                starttimetempser__gte=starttime,
                starttimetempser__lte=finishtime
            )
            serializer = TemporaryseriesSerializer(TSs_within_interval, many=True)
            response_data = [{'starttimetempser': item['starttimetempser'], 'value': item[value], 'type' : item['ideventtype']} for item in serializer.data]

            return Response({'results': response_data})
        except Exception as e:
            return Response({'error': str(e)})
from rest_framework.pagination import PageNumberPagination      
class TempSeriesCompletePerTime(generics.ListAPIView):
    """
    Sericio que recopila Series Temporales almacenados en la BD local con detalles completos ,respondiendo a un intervalo de tiempo con un formato especifico
    """
    queryset = Temporaryseries.objects.all()
    serializer_class = TemporaryseriesSerializer
    pagination_class = PageNumberPagination
    pagination_class.page_size = 10
    filter_backends = [filters.OrderingFilter]
    ordering_fields = '__all__'  # Campos por los que se puede ordenar

    def get_queryset(self):
        idstation = self.kwargs['idstation']
        starttime = datetime.strptime(self.kwargs['starttime'], '%Y-%m-%dT%H:%M:%S.%f')
        finishtime = datetime.strptime(self.kwargs['finishtime'], '%Y-%m-%dT%H:%M:%S.%f')

        queryset = self.queryset.filter(
            Q(idstation=idstation),
            starttimetempser__gte=starttime,
            starttimetempser__lte=finishtime
        )
        return queryset


from rest_framework.pagination import PageNumberPagination

from obspy.clients.earthworm import Client
from obspy import UTCDateTime
import time

class TempSeriesOBSPerTime(generics.GenericAPIView):
    """
    Sericio que selecciona las Series Temporales recopiladas por OBSPY ,respondiendo a un intervalo de tiempo con un formato especifico
    """
    queryset = [] 
    def get(self, request, idstation, starttime, finishtime , value='waveskewnesstempser'):
        try:
            #starttime = datetime.strptime(starttime, '%Y-%m-%dT%H:%M:%S.%f')
            #finishtime = datetime.strptime(finishtime, '%Y-%m-%dT%H:%M:%S.%f')
            t1 = UTCDateTime(starttime)
            t2 = UTCDateTime(finishtime)
            client = Client("10.0.20.55",16025)
            st = client.get_waveforms("PE", idstation, "", "BH?", t1, t2)

            #lapsemin = int(lapsemin)
            #starttime = starttime - timedelta(hours=6)
            '''TSs_within_interval = Temporaryseries.objects.filter(
                Q(idstation=idstation),
                starttimetempser__gte=starttime,
                starttimetempser__lte=finishtime
            )'''
            
            trace = st[0]  # Suponiendo que st es la lista de traces que obtuviste de ObsPy
            # Accede a los valores de la serie temporal y los tiempos correspondientes
            values = trace.data
            times = trace.times()

            # Genera una lista de diccionarios con la información requerida
            # = [{'starttimetempser': time, 'value': value, 'type': "NOC"} for time, value in zip(times, values)]
            response_data = [{"time": time, "value": value, 'type': "NOC"} for time, value in zip(times, values)]

            #serializer = TemporaryseriesSerializer(TSs_within_interval, many=True)
            #response_data = [{'starttimetempser': item['starttimetempser'], 'value': item[value], 'type' : item['ideventtype']} for item in serializer.data]
            return Response({'results': response_data})
        
        except Exception as e:
            return Response({'error': str(e)})
        


from obspy import Stream, Trace


class TempSeriesOBSCantPerTime(generics.GenericAPIView):
    """
    Sericio que selecciona las Series Temporales recopiladas por OBSPY ,respondiendo a un intervalo de tiempo con un formato especifico
    """
    queryset = [] 
    def get(self, request, idstation, starttime, finishtime, cantidad , value='waveskewnesstempser'):
        try:
            segmento =  100 // cantidad
            #starttime = datetime.strptime(starttime, '%Y-%m-%dT%H:%M:%S.%f')
            #finishtime = datetime.strptime(finishtime, '%Y-%m-%dT%H:%M:%S.%f')
            t1 = UTCDateTime(starttime)
            t2 = UTCDateTime(finishtime)
            client = Client("10.0.20.55",16025)
            st = client.get_waveforms("PE", idstation, "", "BH?", t1, t2)

            #lapsemin = int(lapsemin)
            #starttime = starttime - timedelta(hours=6)
            '''TSs_within_interval = Temporaryseries.objects.filter(
                Q(idstation=idstation),
                starttimetempser__gte=starttime,
                starttimetempser__lte=finishtime
            )'''
            
            trace = st[0]  # Suponiendo que st es la lista de traces que obtuviste de ObsPy
            # Accede a los valores de la serie temporal y los tiempos correspondientes
            stream = Stream(traces=[trace])
            stream.decimate(segmento, strict_length=False, no_filter=True)
            #values = trace.data
            times = trace.times()
            # Genera una lista de diccionarios con la información requerida
            # = [{'starttimetempser': time, 'value': value, 'type': "NOC"} for time, value in zip(times, values)]
            response_data = [{"time": time, "value": value, 'type': "NOC"} for time, value in zip(times, values)]

            #serializer = TemporaryseriesSerializer(TSs_within_interval, many=True)
            #response_data = [{'starttimetempser': item['starttimetempser'], 'value': item[value], 'type' : item['ideventtype']} for item in serializer.data]
            return Response({'results': response_data})
        
        except Exception as e:
            return Response({'error': str(e)})
#----------------------------------------------------------------------MaskImgRawPerTime
class BlobsStationperMask(generics.GenericAPIView):
    """
    Sericio que recopila Los Blobs con detalle de estacion, pertenecientes a una Mascara en especifico
    """
    queryset = []  # Define una consulta ficticia

    def get(self, request, idmask):
      
            mask= Mask.objects.get(idmask = idmask)
            blobs = Blob.objects.filter(idmask=idmask)
            results = []
            results.append({
                'Station': StationSerializer(mask.idstation).data,
                'Blobs': BlobSerializer(blobs, many=True).data,
            })
            return Response({'results': results})
     
#----------------------------------------------------------------------MaskImgRawPerTime

class MaskImgRawPerTime(generics.GenericAPIView):
    """
    Sericio que recopila Imagenes Raw con sus Mascaras pertenecintes respondiendo a un intervalo de tiempo con un formato especifico
    """
    queryset = []  # Define una consulta ficticia

    def get(self, request, idstation, starttime, finishtime):
        try:
            idstation = idstation
            starttime = datetime.strptime(starttime, '%Y-%m-%dT%H:%M:%S.%f')
            finishtime = datetime.strptime(finishtime, '%Y-%m-%dT%H:%M:%S.%f')
            #lapsemin = int(lapsemin)
            #starttime = starttime - timedelta(hours=6)
            masks_within_interval = Mask.objects.filter(
                Q(idmask__idstation=idstation),
                starttimemask__gte=starttime,
                starttimemask__lte=finishtime
            )
            results = []
            for mask in masks_within_interval:
                segmentation_image = Imagesegmentation.objects.get(idphoto=mask.idmask.idphoto)
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
    """
    Sericio de registro de Usuarios
    """
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
    """
    Sericio de inicio de Sesion
    """
    
    permission_classes = (permissions.AllowAny,)
    @swagger_auto_schema( request_body=AuthTokenSerializer)

    def post(self, request, format=None):
        if 'email' not in request.data or 'password' not in request.data:
            return Response({'error': 'Se requieren los campos "email" y "password" en la solicitud.'}, status=400)

        email = request.data.get('email')
        password = request.data.get('password')

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
    """
    Sericio retorno de detalles de usuario a partir del token de sesion
    """
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
    """
    Sericio de envio de correo 
    """
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
    """
    Sericio CRUD de Alerta generada
    """
    queryset = Alert.objects.order_by('pk')
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
    """
    Sericio CRUD de Configuracionde Alerta para Volcanes
    """
    queryset = Alertconfiguration.objects.order_by('pk')
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
    """
    Sericio CRUD de Blobs
    """
    queryset = Blob.objects.order_by('pk')
    serializer_class = BlobSerializer


class EventtypeViewSet(ModelViewSet):
    """
    Sericio CRUD de Tipos de Eventos
    """
    queryset = Eventtype.objects.order_by('pk')
    serializer_class = EventtypeSerializer


class HistoryViewSet(ModelViewSet):
    """
    Sericio CRUD de Historial
    """
    queryset = History.objects.order_by('pk')
    serializer_class = HistorySerializer


class ImagesegmentationViewSet(ModelViewSet):
    """
    Sericio CRUD de Raw Imagen
    """
    queryset = Imagesegmentation.objects.order_by('pk')
    serializer_class = ImagesegmentationSerializer


class MaskViewSet(ModelViewSet):
    """
    Sericio CRUD de Mascaras
    """
    queryset = Mask.objects.order_by('pk')
    serializer_class = MaskSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter,filters.SearchFilter]
    #pagination_class = None

class AshdispersionViewSet(ModelViewSet):
    """
    Sericio CRUD de Dispesion de Ceniza
    """
    queryset = Ashdispersion.objects.order_by('pk')
    serializer_class = AshdispersionSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter,filters.SearchFilter]

class AshfallpredictionViewSet(ModelViewSet):
    """
    Sericio CRUD de prediccion en la caida de Cenizas
    """
    queryset = Ashfallprediction.objects.order_by('pk')
    serializer_class = AshfallpredictionSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter,filters.SearchFilter]

class WinddirectionViewSet(ModelViewSet):
    """
    Sericio CRUD de Direccion del viento
    """
    queryset = Winddirection.objects.order_by('pk')
    serializer_class = WinddirectionSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter,filters.SearchFilter]


class StationViewSet(ModelViewSet):
    """
    Sericio CRUD de Estacion
    """
    queryset = Station.objects.order_by('pk')
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
        queryset = Station.objects.all()
        data = StationSerializer(queryset, many=True).data
        return Response(data)
    
class TemporaryseriesViewSet(ModelViewSet):
    """
    Sericio CRUD de Series Temporales
    """
    queryset = Temporaryseries.objects.order_by('pk')
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter,filters.SearchFilter]
    serializer_class = TemporaryseriesSerializer
class MappingViewSet(ModelViewSet):
    """
    Sericio CRUD de Mapeo para los atributos de las tablas
    """
    queryset = Mapping.objects.order_by('pk')
    serializer_class = MappingSerializer


class UserPViewSet(ModelViewSet):
    """
    Sericio CRUD de Usuarios
    """
    queryset = UserP.objects.order_by('pk')
    serializer_class = UserPSerializer
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter,filters.SearchFilter]
    filterset_class = volcanoApp.filters.UserPFilter 

    def all(self, request):
        queryset = UserP.objects.all()
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
    """
    Servicio CRUD para Volcano
    """
    queryset = Volcano.objects.order_by('pk')
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
        """
        listado de todos los volcanes
        """
        queryset = Volcano.objects.all()
        data = VolcanoSerializer(queryset, many=True).data
        return Response(data)
    
from django.shortcuts import render
from django.db.models import Count
from django.db.models.functions import TruncMonth


class ContarRegistrosAPIView(APIView):
    """
    Servicio de Dsahboard conteo de registros en diferentes tablas
    """
    def get(self, request, *args, **kwargs):
        # Realizar el conteo de registros en diferentes modelos
        cantidad_registrosUserp = UserP.objects.count()
        cantidad_registrosVolcanes = Volcano.objects.count()
        cantidad_registrosEstaciones = Station.objects.count()
        cantidad_registrosAlert = Alert.objects.count()
        ultimos3_alert = Alert.objects.all().order_by('-datecreationalert')[:3]
        ultimos3_alert_serialized = AlertSerializer(ultimos3_alert, many=True, context={'request': request}).data
        # Obtener el conteo de alertas por volcán y usuarios por país
        conteo_alertas_por_volcan = list(Alert.objects.values('idvolcano__shortnamevol').annotate(total_alertas=Count('idvolcano')))
        usuarios_por_pais = list(UserP.objects.values('country').annotate(total_usuarios=Count('country')))
        

      
        caracterizaciones= Mask.objects.count()
        Series_Temporales= Temporaryseries.objects.count()
        Ash_dispersion= Ashdispersion.objects.count()
        Wind_direction= Winddirection.objects.count()
        Ashfall_prediction = Ashfallprediction.objects.count()

        alertas_por_mes = Alert.objects.annotate(
            mes=TruncMonth('datecreationalert')
        ).values('mes').annotate(
            total_alertas_mes=Count('idalert')
        ).order_by('mes')
        # Formatear los resultados
        alerta_por_mes = [
            {
                'mes': alerta['mes'].strftime('%Y-%m'),
                'total_alertas_mes': alerta['total_alertas_mes']
            }
            for alerta in alertas_por_mes
        ]
        

        # Devolver el conteo como JSON
        return Response({
            'cantidad_registrosUserp': cantidad_registrosUserp,
            'cantidad_registrosVolcanes': cantidad_registrosVolcanes,
            'cantidad_registrosEstaciones': cantidad_registrosEstaciones,
            'cantidad_registrosAlert': cantidad_registrosAlert,
            'ultimos3_alert': ultimos3_alert_serialized,
            'alerts_por_volcan': conteo_alertas_por_volcan,
            'usuarios_por_pais': usuarios_por_pais,
            'caracterizaciones': caracterizaciones,
            'Ash_dispersion' : Ash_dispersion, 
            'Series_Temporales' : Series_Temporales, 
            'Wind_direction' :Wind_direction , 
            'Ashfall_prediction' : Ashfall_prediction, 
            'alerta_por_mes' :alerta_por_mes 


        }, status=status.HTTP_200_OK)
    
def index(request):
    channel_layer = get_channel_layer()

    # Definir el mensaje que deseas enviar
    message = {
        "type": "chat.message",  # Tipo de mensaje (puede ser cualquier identificador)
        "text": "Hola desde la vista!",  # Contenido del mensaje
    }

    # Enviar el mensaje a través del canal "chat" a todos los clientes conectados
    async_to_sync(channel_layer.group_send)("volcan_yei", {
        "type": "chat.message",  # Tipo de mensaje (debe coincidir con el tipo en consumers.py)
        "message": json.dumps(message),  # Convertir el mensaje a JSON para el envío
    })
    async_to_sync(channel_layer.send)('yei', {"type": "chat.message","message": "Hola a todos en esta sala!" })
    return HttpResponse("Hola mundo")


def pushnotif(request):
    return render(request, 'websocket/pushnotif.html')

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def room(request):
    return render(request, "chat/room.html")


from django.shortcuts import render



# views.py
from django.http import JsonResponse
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .consumers import notifpush
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import JsonResponse
def enviar_alerta(request):
    try:
        channel_layer = get_channel_layer()

        # Enviar un mensaje al consumidor de WebSocket
        message_from_server = {'message': 'Notificación desde otro lugar de la aplicación'}
        group_name = "canal_notif_alert"  # El nombre del grupo al que deseas enviar el mensaje

        # Enviar el mensaje a través del canal de capas con el nuevo tipo de mensaje
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "send.notification_from_server",  # Tipo de mensaje definido en el consumidor
                "message": message_from_server
            }
        )

        return JsonResponse({'status': 'success', 'message': 'Alerta enviada correctamente'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
def abrir_socket(request):
    return render(request, 'tu_template.html')

def ejemplo_realtime(request):
    return render(request, 'realtime/base.html', context={'text': 'Hello'})

