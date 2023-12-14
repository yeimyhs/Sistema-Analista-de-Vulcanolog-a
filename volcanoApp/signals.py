from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from volcanoApp.models import UserP, Alert

from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import logging
logger = logging.getLogger(__name__)

@receiver(post_save, sender=Alert)
def enviar_notificacion(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    mensaje = {
        'tipo': 'nueva_notificacion',
        'mensaje': 'Se ha guardado un nuevo objeto',
        'id_alerta': instance  # Puedes enviar detalles relevantes sobre la alerta
    }
    # Obtener el canal específico para el volcán asociado a la alerta
    canal_volcan = f"volcan_{instance.idvolcano.shortnamevol}"  # Suponiendo que 'idvolcano' es el campo ForeignKey en Alert
        
    # Enviar el mensaje al canal específico del 
    print("==============================",canal_volcan)
    # Agregar mensaje de registro para verificar el envío
    logger.info(f"Enviando mensaje al canal: {canal_volcan}. Contenido: {mensaje}")
    
    # Enviar el mensaje al canal específico del volcán
    async_to_sync(channel_layer.group_send)(canal_volcan, {"type": "enviar_mensaje", "contenido": mensaje})
@receiver(post_save, sender=UserP)
def sync_userp_data(sender, instance, **kwargs):
    try:
        user = User.objects.get(pk=instance.id_id)
        user.username = instance.names
        user.email = instance.email
        user.save()
    except User.DoesNotExist:
        pass
