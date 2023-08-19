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

#------------------------------------------------------------------------------documentacion
schema_view = get_schema_view(
   openapi.Info(
      title="Lonccosv3 API",
      default_version='v3',
      description="Diverticuentos",
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


urlpatterns = [
    path('register/', views.RegisterAPI.as_view(), name='register'),
    path('login/', views.LoginAPI.as_view(), name='login'),
    path('logout/', decorated_logout_view, name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),#cuando inicia sesion en varios browser y quiere salir de todos
    path('userbyToken/', views.UserAPI.as_view()),

    re_path(r'^swagger(<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
router = SimpleRouter()

router.register(r'alert', views.AlertViewSet)
router.register(r'alertconfiguration', views.AlertconfigurationViewSet)
router.register(r'blob', views.BlobViewSet)
router.register(r'eventtype', views.EventtypeViewSet)
router.register(r'history', views.HistoryViewSet)
router.register(r'imagesegmentation', views.ImagesegmentationViewSet)
router.register(r'mask', views.MaskViewSet)
router.register(r'meteorologicaldata', views.MeteorologicaldataViewSet)
router.register(r'station', views.StationViewSet)
router.register(r'temporaryseries', views.TemporaryseriesViewSet)
router.register(r'userp', views.UserPViewSet)
router.register(r'volcano', views.VolcanoViewSet)

urlpatterns += router.urls
