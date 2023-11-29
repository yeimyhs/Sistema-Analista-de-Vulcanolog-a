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
def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Solicitud de restablecimiento de contraseña"
					email_template_name = "password_reset/password_reset_email.html"
					c = {
					"email":user.email,
					'domain':settings.DOMAIN,
					'site_name': 'Diverticuentos',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
                    
					try:
						send_mail(subject, strip_tags(email), settings.EMAIL_HOST_USER , [user.email], html_message=email)
					except BadHeaderError:
						return HttpResponse('Envio no realizado')
                    
					return redirect ("/volcanoApp/password_reset/done/")
            
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="password_reset/password_reset.html", context={"password_reset_form":password_reset_form})

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
class TempSeriesPerTime(generics.GenericAPIView):
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
        recipient_list= request.data[settings.EMAIL_HOST_USER]
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
    filterset_class = volcanoApp.filters.AlertFilter 

'''    pagination_class = CustomPagination 

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
'''

class AlertconfigurationViewSet(ModelViewSet):
    queryset = Alertconfiguration.objects.filter(statealertconf=1).order_by('pk')
    serializer_class = AlertconfigurationSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter,filters.SearchFilter]

    
    def all(self, request):
        queryset = Alertconfiguration.objects.all()
        data = AlertconfigurationSerializer(queryset, many=True).data
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
                  'altitudevol', 'pwavespeedvol', 'densityvol', 'attcorrectfactorvol']


    def all(self, request):
        queryset = Volcano.objects.filter(statevol=1)
        data = VolcanoSerializer(queryset, many=True).data
        return Response(data)