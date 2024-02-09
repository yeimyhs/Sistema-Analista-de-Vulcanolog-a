from rest_framework.viewsets import ModelViewSet
from volcanoApp.serializers import AlertSerializer, AlertconfigurationSerializer, BlobSerializer, EventtypeSerializer, HistorySerializer, ImagesegmentationSerializer, MaskSerializer, StationSerializer, TemporaryseriesSerializer, VolcanoSerializer \
    , UserPSerializer ,MappingSerializer, AshdispersionSerializer, WinddirectionSerializer, AshfallpredictionSerializer , AlarmSerializer,ExplosionSerializer
from volcanoApp.models import Alert, Alertconfiguration, Blob, Eventtype, History, Imagesegmentation, Mask, Station, Temporaryseries, Volcano \
    , UserP, Mapping, Ashdispersion, Ashfallprediction, Winddirection, Explosion,Alarm
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

    def get(self, request, idstation, starttime, finishtime, value='relativeheight'):
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
            response_data = [{'starttimetempser': item['starttimetempser'], 'value': item[value], 'durationtempser' : item['durationtempser'], 'type' : item['ideventtype']} for item in serializer.data]

            return Response({'results': response_data})
        except Exception as e:
            return Response({'error': str(e)})
        
class TempSeriesPerTimeType(generics.GenericAPIView):
    """
    Sericio que recopila Series Temporales locales ,respondiendo a un intervalo de tiempo con un formato especifico
    """
    queryset = []  # Define una consulta ficticia

    def get(self, request, idstation, starttime, finishtime, eventtype , value='relativeheight'):
        try:
            idstation = idstation
            starttime = datetime.strptime(starttime, '%Y-%m-%dT%H:%M:%S.%f')
            finishtime = datetime.strptime(finishtime, '%Y-%m-%dT%H:%M:%S.%f')
            #lapsemin = int(lapsemin)
            #starttime = starttime - timedelta(hours=6)
            TSs_within_interval = Temporaryseries.objects.filter(statetempser=1).filter(
                Q(idstation=idstation),
                Q(ideventtype=eventtype),
                starttimetempser__gte=starttime,
                starttimetempser__lte=finishtime
            )
            serializer = TemporaryseriesSerializer(TSs_within_interval, many=True)
            response_data = [{'starttimetempser': item['starttimetempser'], 'value': item[value], 'durationtempser' : item['durationtempser'], 'type' : item['ideventtype']} for item in serializer.data]

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
    def get(self, request, idstation, starttime, finishtime , value='relativeHeight'):
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
    def get(self, request, idstation, starttime, finishtime, cantidad , value='relativeHeight'):
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
#----------------------------------------------------------------------MaskImgRawPerTime
class BlobsStationperMask(generics.GenericAPIView):
    """
    Sericio que recopila Los Blobs con detalle de estacion y el volcan, pertenecientes a una Mascara en especifico
    """
    queryset = []  # Define una consulta ficticia

    def get(self, request, idmask):
      
            mask= Mask.objects.get(idmask = idmask)
            image= Imagesegmentation.objects.get(idphoto = idmask)
            station= mask.idstation
            volcano= station.idvolcano
            blobs = Blob.objects.filter(idmask=idmask)
            results = []
            results.append({
                'Volcano':VolcanoSerializer(volcano).data,
                'Station': StationSerializer(station).data,
                'Blobs': BlobSerializer(blobs, many=True).data,
                'imgRaw': ImagesegmentationSerializer(image).data,
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

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action  # Add this import
from rest_framework.response import Response
class MaskViewSet(ModelViewSet):
    """
    Sericio CRUD de Mascaras
    """
    queryset = Mask.objects.order_by('pk')
    serializer_class = MaskSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter,filters.SearchFilter]
    #pagination_class = None

    @action(detail=True, methods=['get'])
    def nearby_masks(self, request, pk=None):
        """
        Obtener el Mask siguiente y anterior más cercano en función de la fecha starttimemask
        junto con los correspondientes Imagesegmentation de ambos.
        """
        current_mask = get_object_or_404(Mask, pk=pk)
        queryset = Mask.objects.order_by('starttimemask')

        previous_mask = queryset.filter(starttimemask__lt=current_mask.starttimemask).last()
        next_mask = queryset.filter(starttimemask__gt=current_mask.starttimemask).first()

        if previous_mask:
            previous_imagesegmentation = previous_mask.idmask
        else:
            previous_imagesegmentation = None

        if next_mask:
            next_imagesegmentation = next_mask.idmask
        else:
            next_imagesegmentation = None

        data = {
            'previous_mask': MaskSerializer(previous_mask).data if previous_mask else None,
            'previous_imagesegmentation': ImagesegmentationSerializer(previous_imagesegmentation).data if previous_imagesegmentation else None,
            'current_mask': MaskSerializer(current_mask).data,
            'current_imagesegmentation': ImagesegmentationSerializer(current_mask.idmask).data,
            'next_mask': MaskSerializer(next_mask).data if next_mask else None,
            'next_imagesegmentation': ImagesegmentationSerializer(next_imagesegmentation).data if next_imagesegmentation else None,
        }

        return Response(data)
    
    @action(detail=True, methods=['get'])
    def find_related_masks(self, request, pk=None):
        """
        Encuentra máscaras relacionadas basadas en la estación y el tiempo de inicio.
        """
        mask = get_object_or_404(Mask, pk=pk)

        # Obtener el id de la estación asociada a la máscara
        station_id = mask.idstation_id

        # Encontrar el id del volcán asociado a la estación
        try:
            station = Station.objects.get(idstation=station_id)
            volcano_id = station.idvolcano_id
        except Station.DoesNotExist:
            return Response({'detail': 'Estación no encontrada'}, status=404)

        # Encontrar estaciones gráficas asociadas al volcán
        graphic_stations = Station.objects.filter(idvolcano=volcano_id, typestat=2)  # Suponiendo que el tipo gráfico es 2

        # Inicializar la variable que indica si se encontró una estación gráfica
        found_graphic_station = False

        # Inicializar el diccionario para almacenar la información relacionada con cada estación gráfica
        related_data_by_station = {}


        # Encontrar máscaras relacionadas con el mismo starttimemask o con una calibración de tiempo de 10 segundos
        for graphic_station in graphic_stations:
            try:
                related_mask = Mask.objects.get(
                    idstation=graphic_station.idstation,
                    starttimemask__range=(mask.starttimemask, mask.starttimemask + timedelta(seconds=10))
                )
                related_imagesegmentation = related_mask.idmask

                related_data_by_station[graphic_station.idstation] = {
                    'found_graphic_station': True,
                    'related_mask': MaskSerializer(related_mask).data,
                    'related_imagesegmentation': ImagesegmentationSerializer(related_imagesegmentation).data,
                }

                found_graphic_station = True
            except Mask.DoesNotExist:
                related_data_by_station[graphic_station.idstation] = {
                    'found_graphic_station': False,
                    'related_mask': None,
                    'related_imagesegmentation': None,
                }

        response_data = {
            'found_graphic_station': found_graphic_station,
            'related_data_by_station': related_data_by_station,
        }

        return Response(response_data)
    
@api_view(['GET'])
def find_common_start_time(request):
    """
    Encuentra un starttimemask que tenga máscaras existentes en cada estación.
    """
    # Obtener todas las estaciones
    stations = Station.objects.all()

    # Inicializar el diccionario para almacenar el starttimemask común por estación
    common_start_time_by_station = {}

    # Iterar sobre todas las estaciones
    for station in stations:
        # Encontrar el starttimemask más temprano para la estación actual
        min_start_time = Mask.objects.filter(idstation=station.idstation).aggregate(Min('starttimemask'))['starttimemask__min']

        # Verificar si se encontró algún starttimemask
        if min_start_time is not None:
            # Añadir el starttimemask más temprano al diccionario
            common_start_time_by_station[station.idstation] = min_start_time
        else:
            # Si no se encontró, devolver un mensaje indicando que no hay starttimemask
            return Response({'detail': f'No se encontró starttimemask para la estación {station.idstation}'})

    # Encontrar el starttimemask común máximo entre todas las estaciones
    common_start_time = max(common_start_time_by_station.values())

    # Devolver el starttimemask común
    return Response({'common_start_time': common_start_time})
    
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
    search_fields = ['idstation__longnamevol','starttimetempser','idstation__shortnamestat']
    filterset_fields = {
        'idstation': ['exact'],#, 'icontains'
        'starttimetempser': ['exact', 'gte', 'lte', 'date'], # Permitir búsqueda exacta, mayor que, menor que, y por fecha
        'idstation__shortnamestat': ['exact', 'icontains'],
    }
    serializer_class = TemporaryseriesSerializer

class ExplosionViewSet(ModelViewSet):
    """
    Sericio CRUD de Explosion
    """
    queryset = Explosion.objects.order_by('pk')
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter,filters.SearchFilter]
    search_fields = ['idstation__longnamevol','starttime','idstation__shortnamestat']
    filterset_fields = {
        'idvolcano': ['exact'],#, 'icontains'
        'idstation': ['exact'],#, 'icontains'
        'starttime': ['exact', 'gte', 'lte', 'date'], # Permitir búsqueda exacta, mayor que, menor que, y por fecha
        'idstation__shortnamestat': ['exact', 'icontains'],
    }
    serializer_class = ExplosionSerializer
class AlarmViewSet(ModelViewSet):
    """
    Sericio CRUD de Alarma
    """
    queryset = Alarm.objects.order_by('pk')
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter,filters.SearchFilter]
    search_fields = ['idstation__longnamevol','starttime','idstation__shortnamestat']
    filterset_fields = {
        'idvolcano': ['exact'],#, 'icontains'
        'idstation': ['exact'],#, 'icontains'
        'starttime': ['exact', 'gte', 'lte'], # Permitir búsqueda exacta, mayor que, menor que, y por fecha
        'idstation__shortnamestat': ['exact', 'icontains'],
    }
    serializer_class = AlarmSerializer

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

    @action(detail=False, methods=['get'])
    def volcano_type_stations(self, request):
        """
        Obtener información de todos los volcanes con arrays de estaciones sísmicas y visuales.
        """
        volcanoes = Volcano.objects.all()
        volcano_data = []

        for volcano in volcanoes:
            seismic_stations = Station.objects.filter(idvolcano=volcano.idvolcano, typestat=1)  # Suponiendo que el tipo sísmico es 1
            visual_stations = Station.objects.filter(idvolcano=volcano.idvolcano, typestat=2)   # Suponiendo que el tipo visual es 2

            seismic_stations_data = [{'id': station.idstation, 'shortname': station.shortnamestat, 'longname': station.longnamestat} for station in seismic_stations]
            visual_stations_data = [{'id': station.idstation, 'shortname': station.shortnamestat, 'longname': station.longnamestat} for station in visual_stations]

            volcano_info = {
                'idvolcano': volcano.idvolcano,
                'shortnamevol': volcano.shortnamevol,
                'longnamevol': volcano.longnamevol,
                'seismic_stations': seismic_stations_data,
                'visual_stations': visual_stations_data,
            }

            volcano_data.append(volcano_info)

        return Response(volcano_data)
    
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

