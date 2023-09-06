from django.test import TestCase
from rest_framework.test import APIClient
from volcanoApp.models import Volcano
from rest_framework import status
from django.urls import reverse
class VolcanoCRUDTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.volcano_data = {
            'shortnamevol': 'TestVolcano',
            'longnamevol': 'Test Volcano Name',
            'descriptionvol': 'Test description of volcano',
            'latitudevol': 0.0,
            'longitudevol': 0.0,
            'altitudevol': 1000.0,
            'pwavespeedvol': 2000.0,
            'densityvol': 2.5,
            'attcorrectfactorvol': 1.0,
            'indvol': 1,
            'statevol': 1,
        }
        self.volcano = Volcano.objects.create(**self.volcano_data)

    def tearDown(self):
        self.volcano.delete()
    def test_read_volcano(self):
        response = self.client.get('/volcanoApp/volcano/')
        self.assertEqual(response.status_code, 200)  # Debería devolver un código 200 (OK)
        #print(response.data)  # Agrega esta línea para imprimir la respuesta en la consola
        self.assertEqual(Volcano.objects.count(), 1)  # Debería haber un objeto en la respuesta

    def test_create_volcano(self):
        response = self.client.post('/volcanoApp/volcano/', self.volcano_data, format='json')
        self.assertEqual(response.status_code, 201)  # Debería devolver un código 201 (Created)
        self.assertEqual(Volcano.objects.count(), 2)  # Debería haber dos objetos en la base de datos


    def test_update_volcano(self):
        # Crea un objeto de Volcano para actualizar
        volcano = Volcano.objects.create(
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
            datecreationvol="2023-09-06T03:20:11.078889Z"
        )

        # Datos para actualizar el objeto de Volcano
        update_data = {
            "shortnamevol": "UpdatedVolcano",
            "longnamevol": "Updated Volcano Name",
        }

        # Realiza la solicitud PATCH para actualizar el objeto de Volcano
        response = self.client.patch(reverse("volcanoApp:volcano-detail", args=[volcano.pk]), update_data, format="json")
        # Verifica que la respuesta sea un código 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_volcano = Volcano.objects.get(pk=volcano.pk)
        self.assertEqual(updated_volcano.shortnamevol, "UpdatedVolcano")
        self.assertEqual(updated_volcano.longnamevol, "Updated Volcano Name")

    def test_delete_volcano(self):
        response = self.client.delete(f'/volcanoApp/volcano/{self.volcano.idvolcano}/')
        self.assertEqual(response.status_code, 204)  # Debería devolver un código 204 (No Content)
        self.assertEqual(Volcano.objects.count(), 0)  # No debería haber objetos en la base de datos después de eliminarlo
