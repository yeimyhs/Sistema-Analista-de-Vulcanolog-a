from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from volcanoApp.models import Alertconfiguration, Volcano

class AlertconfigurationCRUDTestCase(APITestCase):
    def setUp(self):
        self.volcano = Volcano.objects.create(
            idvolcano = "VOL",
            shortnamevol="TestVol",
            longnamevol="Test Vol",
            descriptionvol="Test descri",
            latitudevol=0.0,
            longitudevol=0.0,
            altitudevol=1000.0,
            pwavespeedvol=2000.0,
            densityvol=2.5,
            attcorrectfactorvol=1.0,
            indvol=1,
            statevol=1,
        )
        self.alert_config = Alertconfiguration.objects.create(
            altitudalertconf=1000.0,
            statealertconf=1,
            idvolcano=  self.volcano,
            startalert= 1,
            messagetemplateconfalert= "MEnsaje predeterminado"

        )
        
    def test_create_alert_config(self):
        volcano = Volcano.objects.create(
            idvolcano = "VO2",
            shortnamevol="TestVol",
            longnamevol="Test Vol",
            descriptionvol="Test descri",
            latitudevol=0.0,
            longitudevol=0.0,
            altitudevol=1000.0,
            pwavespeedvol=2000.0,
            densityvol=2.5,
            attcorrectfactorvol=1.0,
            indvol=1,
            statevol=1,
        )
        create_data = {
            "altitudalertconf": 1500.0,
            "statealertconf": 1,
            "idvolcano":self.volcano.pk,
            "startalert": 1,
            "messagetemplateconfalert": "MEnsaje predeterminado"
        }
        response = self.client.post(reverse("volcanoApp:alertconfiguration-list"), create_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verifica que el objeto se ha creado en la base de datos
        created_alert_config = Alertconfiguration.objects.get(idalertconf=response.data['idalertconf'])
        self.assertEqual(created_alert_config.altitudalertconf, create_data['altitudalertconf'])

    def test_read_alert_config(self):
        response = self.client.get(reverse("volcanoApp:alertconfiguration-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)  # Verifica que se devuelve al menos un objeto

    def test_update_alert_config(self):
        update_data = {
            "altitudalertconf": 2000.0,
        }
        response = self.client.patch(reverse("volcanoApp:alertconfiguration-detail", args=[self.alert_config.idalertconf]), update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Vuelve a obtener el objeto de Alertconfiguration desde la base de datos para verificar los cambios
        updated_alert_config = Alertconfiguration.objects.get(idalertconf=self.alert_config.idalertconf)
        self.assertEqual(updated_alert_config.altitudalertconf, update_data['altitudalertconf'])

    def test_delete_alert_config(self):
        response = self.client.delete(reverse("volcanoApp:alertconfiguration-detail", args=[self.alert_config.idalertconf]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verifica que el objeto se ha eliminado de la base de datos
        with self.assertRaises(Alertconfiguration.DoesNotExist):
            Alertconfiguration.objects.get(idalertconf=self.alert_config.idalertconf)
