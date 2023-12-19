from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from volcanoApp.models import UserP, Alert

from .serializers import AlertPushSerializer
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import logging
import json



@receiver(post_save, sender=Alert)
def enviar_notificacion(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    alert_serializer = AlertPushSerializer(instance)
    mensaje = {
        'mensaje': f'Se ha generado una alerta {alert_serializer.data}',
    }
    # Obtener el canal específico para el volcán asociado a la alerta
    canal_volcan = f"volcan_{instance.idvolcano.idvolcano.lower()}"
    # Enviar el mensaje al canal específico del  
    print("==============================",canal_volcan)
    async_to_sync(channel_layer.group_send)(canal_volcan, {
        "type": "chat.message",  # Tipo de mensaje (debe coincidir con el tipo en consumers.py)
        "message": json.dumps(mensaje),  # Convertir el mensaje a JSON para el envío
    })
    async_to_sync(channel_layer.send)('yei', {"type": "chat.message","message": "Hola a todos en esta sala!" })



@receiver(post_save, sender=UserP)
def sync_userp_data(sender, instance, **kwargs):
    try:
        user = User.objects.get(pk=instance.id_id)
        user.username = instance.names
        user.email = instance.email
        user.save()
    except User.DoesNotExist:
        pass
