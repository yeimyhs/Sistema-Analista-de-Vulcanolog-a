from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from volcanoApp.models import Alert, Volcano, Alertconfiguration

class AlertCRUDTestCase(APITestCase):
    def setUp(self):
        # Crea objetos de Alertconfiguration y Volcano para usar en las pruebas
        self.alert_configuration = Alertconfiguration.objects.create(
            altitudalertconf=1000.0,
            statealertconf=1,
            # Añade otros campos según tu modelo Alertconfiguration
        )

        self.volcano = Volcano.objects.create(
            shortnamevol="TestVolcano",
            longnamevol="Test Volcano Name",
            descriptionvol="Test description of volcano",
            latitudevol=0.0,
            longitudevol=0.0,
            altitudevol=1000.0,
            pwavespeedvol=2000.0,
            densityvol=2.5,
            attcorrectfactorvol=1.0,
            indvol=1,
            statevol=1,
            # Añade otros campos según tu modelo Volcano
        )

        # Crea un objeto de Alert para usar en las pruebas
        self.alert = Alert.objects.create(
            messagealert="Test Message",
            statealert=1,
            idvolcano=self.volcano,
            idalertconf=self.alert_configuration,
            # Añade otros campos según tu modelo Alert
        )
    def test_create_alert(self):
        # Datos para crear un nuevo objeto de Alert
        new_alert_data = {
            "messagealert": "New Test Message",
            "statealert": 2,
            "idvolcano": self.volcano.idvolcano,  # Utiliza el ID del volcán creado en setUp
            "idalertconf": self.alert_configuration.idalertconf,  # Utiliza el ID de la configuración de alerta creado en setUp
        }

        # Realiza una solicitud POST para crear un nuevo objeto de Alert
        response = self.client.post(reverse("volcanoApp:alert-list"), new_alert_data, format="json")

        # Verifica que la respuesta sea un código 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_read_alert(self):
        # Realiza una solicitud GET para obtener detalles del objeto de Alert
        response = self.client.get(reverse("volcanoApp:alert-detail", args=[self.alert.pk]))

        # Verifica que la respuesta sea un código 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_alert(self):
        # Datos para actualizar el objeto de Alert
        update_data = {
            "messagealert": "Updated Message",
            "statealert": 2,
        }

        # Realiza una solicitud PATCH para actualizar el objeto de Alert
        response = self.client.patch(reverse("volcanoApp:alert-detail", args=[self.alert.pk]), update_data, format="json")

        # Verifica que la respuesta sea un código 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Vuelve a obtener el objeto de Alert desde la base de datos para verificar los cambios
        updated_alert = Alert.objects.get(pk=self.alert.pk)

        # Verifica que los campos actualizados coincidan con los valores esperados
        self.assertEqual(updated_alert.messagealert, "Updated Message")
        self.assertEqual(updated_alert.statealert, 2)

    def test_delete_alert(self):
        # Realiza una solicitud DELETE para eliminar el objeto de Alert
        response = self.client.delete(reverse("volcanoApp:alert-detail", args=[self.alert.pk]))

        # Verifica que la respuesta sea un código 204 No Content (que indica que se ha eliminado con éxito)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Verifica que el objeto de Alert ya no exista en la base de datos
        self.assertFalse(Alert.objects.filter(pk=self.alert.pk).exists())
