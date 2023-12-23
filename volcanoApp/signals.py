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


#sirve para notificar dentro del canal una nueva alerta
@receiver(post_save, sender=Alert)
def enviar_notificacion(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    alert_serializer = AlertPushSerializer(instance)
    mensaje = {
        'mensaje': f'Se ha generado una alerta {alert_serializer.data}',
    }
    canal_volcan = "_volcan_push_"
    async_to_sync(channel_layer.group_send)(canal_volcan, {
        "type": "chat.message",  
        "message": json.dumps(mensaje),  
    })

 
#cada que se guarde un usuario profile este se actualizara  en su user django 
@receiver(post_save, sender=UserP)
def sync_userp_data(sender, instance, **kwargs):
    try:
        user = User.objects.get(pk=instance.id_id)
        user.username = instance.names
        user.email = instance.email
        user.save()
    except User.DoesNotExist:
        pass
