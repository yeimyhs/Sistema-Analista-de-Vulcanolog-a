from rest_framework.routers import SimpleRouter
from volcanoApp import views
from django.urls import path , re_path, reverse
#------------------------------------------------------------------------------documentacion imports
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
#------------------------------------------------------------------------------knox imports
from knox import views as knox_views
from django.contrib.auth import views as auth_views

#------------------------------------------------------------------------------documentacion
app_name = 'volcanoApp'

schema_view = get_schema_view(
   openapi.Info(
      title="Volcanov1 API",
      default_version='v1',
      description="Documentation VolcanoApp",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
#----------------------------------------------------------------logout
decorated_logout_view = \
   swagger_auto_schema(
      'Authorization :: header for token authentication'
      #request_body={AuthTokenSerializer}
   )(knox_views.LogoutView.as_view())
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("password_reset/", views.password_reset_request, name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
       template_name='password_reset/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
       template_name="password_reset/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(
       template_name='password_reset/password_reset_complete.html'), name='password_reset_complete'),      
 

    path('register/', views.RegisterAPI.as_view(), name='register'),
    path('login/', views.LoginAPI.as_view(), name='login'),
    path('logout/', decorated_logout_view, name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),#cuando inicia sesion en varios browser y quiere salir de todos
    path('userbyToken/', views.UserAPI.as_view()),
   
   path('', views.index, name='index'),
   path('pushnotifchanel/', views.pushnotif, name='pushnotif'),
   path("chat/", views.room, name="room"),
   #path("password_change", views.password_change, name="password_change"),
   path("winddirectionperttime/<str:idvolcano>/<str:starttime>/<str:finishtime>", views.WinddirectionPertTime.as_view(), name="winddirectionperttime"),
   path("winddirectionperttime/<str:idvolcano>/<str:value>/<str:starttime>/<str:finishtime>", views.WinddirectionPertTime.as_view(), name="winddirectionperttime"),
   #path("winddirectioncompleteperttime/<str:idvolcano>/<str:value>/<str:starttime>/<str:finishtime>", views.WinddirectionCompletePertTime.as_view(), name="winddirectioncompleteperttime"),
   re_path(
        r"winddirectioncompleteperttime/(?P<idvolcano>\w+)/(?P<starttime>[\w\-.:%]+)/(?P<finishtime>[\w\-.:%]+)/",
        views.WinddirectionCompletePertTime.as_view(),
        name="winddirectioncompleteperttime"
    ),
   path("ashfallpredictionperttime/<str:idvolcano>/<str:starttime>/<str:finishtime>", views.AshfallpredictionPertTime.as_view(), name="ashfallpredictionperttime"),
   #path("ashfallpredictioncompleteperttime/<str:idvolcano>/<str:starttime>/<str:finishtime>", views.AshfallpredictionCompletePertTime.as_view(), name="AshfallpredictionCompletePertTime"),
   re_path(
    r"ashfallpredictioncompleteperttime/(?P<idvolcano>\w+)/(?P<starttime>[\w\-.:%]+)/(?P<finishtime>[\w\-.:%]+)/",
    views.AshfallpredictionCompletePertTime.as_view(),
    name="ashfallpredictioncompleteperttime"
),
   path("ashdispersionperttime/<str:idvolcano>/<str:starttime>/<str:finishtime>", views.AshdispersionPertTime.as_view(), name="ashdispersionperttime"),
   path("ashdispersionidnoticeperttime/<str:idvolcano>/<str:idnoticept1>/<str:idnoticept2>/<str:starttime>/<str:finishtime>", views.AshdispersionidNoticePertTime.as_view(), name="ashdispersionidnoticeperttime"),
   path("ashdispersioncompleteperttime/<str:idvolcano>/<str:starttime>/<str:finishtime>", views.AshdispersionCompletePertTime.as_view(), name="ashdispersioncompleteperttime"),
   path("maskimgrawpertime/<str:idstation>/<str:starttime>/<str:finishtime>", views.MaskImgRawPerTime.as_view(), name="MaskImgRawPerTime"),
   path("blobsstationpermask/<str:idmask>", views.BlobsStationperMask.as_view(), name="BlobsStationperMask"),
   path("tempseriespertime/<str:idstation>/<str:value>/<str:starttime>/<str:finishtime>", views.TempSeriesPerTime.as_view(), name="TempSeriesValuePerTime"),
   re_path(
        r"tempseriescompletepertime/(?P<idstation>\w+)/(?P<starttime>[\w\-.:%]+)/(?P<finishtime>[\w\-.:%]+)/",
        views.TempSeriesCompletePerTime.as_view(),
        name="TempSeriesCompletePerTime"
    ),
   path("tempseriespertime/<str:idstation>/<str:starttime>/<str:finishtime>", views.TempSeriesPerTime.as_view(), name="TempSeriesPerTime"),
   path("tempseriesobspertime/<str:idstation>/<str:starttime>/<str:finishtime>", views.TempSeriesOBSPerTime.as_view(), name="TempSeriesOBSPerTime"),
   path("counts", views.ContarRegistrosAPIView.as_view(), name="contar_registros"),
   ##path("meteorologicaldatapertime/<str:idstation>/<str:value>/<str:starttime>/<str:finishtime>", views.MeteorologicalDataPertTime.as_view(), name="MeteorologicalDataPertTime"),
   ##path("meteorologicaldatapertime/<str:idstation>/<str:starttime>/<str:finishtime>", views.MeteorologicalDataPertTime.as_view(), name="MeteorologicalDataPertTime"),
   path('all/alertconfiguration/', views.AlertconfigurationViewSet.as_view({'get': 'all'}), name='alertconfigurations-all'),
   path('all/userp/', views.UserPViewSet.as_view({'get': 'all'}), name='userp-all'),
   path('all/station/', views.StationViewSet.as_view({'get': 'all'}), name='station-all'),
   path('all/volcano/', views.VolcanoViewSet.as_view({'get': 'all'}), name='volcano-all'),

   path('mailer/', views.mailer.as_view()),
    re_path(r'^swagger(<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),




    path('enviar-alerta/', views.enviar_alerta, name='enviar_alerta'),
    path('abrir-socket/', views.abrir_socket, name='abrir_socket'),
    # Otros patrones de URL de tu aplicación...

]

router = SimpleRouter()

router.register(r'alert', views.AlertViewSet)
router.register(r'alertconfiguration', views.AlertconfigurationViewSet)
router.register(r'blob', views.BlobViewSet)
router.register(r'eventtype', views.EventtypeViewSet)
router.register(r'history', views.HistoryViewSet)
router.register(r'imagesegmentation', views.ImagesegmentationViewSet)
router.register(r'mask', views.MaskViewSet)
router.register(r'ashdispersion', views.AshdispersionViewSet)
router.register(r'ashfallprediction', views.AshfallpredictionViewSet)
router.register(r'winddirection', views.WinddirectionViewSet)
router.register(r'station', views.StationViewSet)
router.register(r'temporaryseries', views.TemporaryseriesViewSet)
router.register(r'userp', views.UserPViewSet)
router.register(r'volcano', views.VolcanoViewSet)
router.register(r'mapping', views.MappingViewSet)

urlpatterns += router.urls
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)