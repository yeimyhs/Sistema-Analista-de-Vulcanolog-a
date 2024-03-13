from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from volcanoApp.models import UserP, Alert, Mask, Alertconfiguration, Volcano, Alarm


from .serializers import AlertPushSerializer, AlarmPushSerializer
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import logging
import json

import requests
from django.conf import settings


#sirve para notificar dentro del canal una nueva alerta
@receiver(post_save, sender=Alert)
def enviar_notificacion(sender, instance, **kwargs):
    alertconf = instance.idalertconf
    if alertconf.statealertconf and alertconf.startalert and alertconf.notificationalertconf :
    
        channel_layer = get_channel_layer()
        alert_serializer = AlertPushSerializer(instance)
        message_from_server = {
            'message': f'Se ha generado una alerta {alert_serializer.data}',
        }
        group_name = "canal_notif_alert"  # El nombre del grupo al que deseas enviar el mensaje
        
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "send.notification_from_server",  # Tipo de mensaje definido en el consumidor
                "message": message_from_server 
            }
        )

 
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

@receiver(post_save, sender=Mask)
def generate_alerts_on_mask_save(sender, instance, created, **kwargs):
    #if created:  # Solo ejecutar la lógica si se está creando una nueva instancia de Mask
    idmask= instance.idmask
    idvolcano = idmask.idstation.idvolcano
    alertconf = Alertconfiguration.objects.filter(idvolcano=idvolcano).first()

    if alertconf is not None and alertconf.startalert == 1:
        #volcanoobj = Volcano.objects.get(idvolcano=idvolcano)
        if instance.heighmask > alertconf.altitudalertconf:
            alert_message = (
                f"Se realizó una emisión volcánica con el siguiente detalle:\n"
                f"- Altura de la emisión: {instance.heighmask}\n"
                f"- Nivel de alerta: {idvolcano.alertlevelvol}\n"
                f"- Longitud del volcán: {idvolcano.longitudevol}\n"
                f"- Latitud del volcán: {idvolcano.latitudevol}\n"
                f"- Estacion: {instance.idstation.longnamestat}\n"
                f"- Identificador Imagen Raw: {idmask.idphoto}\n"

            )
            nueva_alerta = Alert(
                messagealert=alertconf.messagetemplateconfalert,
                statealert=1,
                idvolcano=idvolcano,
                idalertconf=alertconf,

                longitudealert = idvolcano.longitudevol,
                latitudealert = idvolcano.latitudevol,
                heighalert=instance.heighmask,
                idstation=instance.idstation,
                alertlevelalert=idvolcano.alertlevelvol,
                typealert = 0, #autogenerado #manual

                idimgraw = idmask

            )
            nueva_alerta.save()
            message = alertconf.messagetemplateconfalert
            if alertconf.mensajeriaalertconf == 1:
                url = f"https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/sendMessage?chat_id={settings.TELEGRAM_CHANNEL_CHAT_ID}&text={alert_message}"
                requests.get(url).json()#)


@receiver(post_save, sender=Alarm)
def generate_nt_ws_alarm_on_save(sender, instance, created, **kwargs):
    #if created:  # Solo ejecutar la lógica si se está creando una nueva instancia de Mask
    alarm_message = (
            f"Se ha generado una nueva alarma con el siguiente detalle:\n"
            f"- Hora de inicio: {instance.starttime}\n"
            f"- Tipo de alarma: {instance.alarmtype}\n"
            f"- ID de la explosión: {instance.idexplosion}\n"
            f"- Volcán: {instance.idvolcano.longnamevol}\n"
            f"- Estación: {instance.idstation.longnamestat}\n"
            f"- Índice: {instance.ind}\n"
        )

    url = f"https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/sendMessage?chat_id={settings.TELEGRAM_CHANNEL_CHAT_ID}&text={alarm_message}"
    requests.get(url).json()#)


@receiver(post_save, sender=Alarm)
def enviar_notificacion_alarma(sender, instance, **kwargs):
    
    channel_layer = get_channel_layer()
    alarm_serializer = AlarmPushSerializer(instance)
    message_from_server = {
        'message': f'Se ha generado una alarma :{alarm_serializer.data}',
    }
    group_name = "canal_notif_alert"  # El nombre del grupo al que deseas enviar el mensaje
    
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "send.notification_from_server",  # Tipo de mensaje definido en el consumidor
            "message": message_from_server
        }
    )