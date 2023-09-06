
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from volcanoApp.models import Station

class StationCRUDTestCase(APITestCase):
    def setUp(self):
        # Crea un objeto de Station para usar en las pruebas
        self.station = Station.objects.create(
            standardnamestat="TestStandard",
            shortnamestat="TestShort",
            longnamestat="Test Long Station Name",
            starttimestat="2023-09-06T03:20:11.078889Z",
            latitudestat=0.0,
            longitudestat=0.0,
            altitudestat=1000.0,
            indstat=1,
            statestat=1,
            typestat=2  # Este campo es opcional, ajusta según tu modelo
        )

    def test_create_station(self):
        # Datos para crear un nuevo objeto de Station
        new_station_data = {
            "standardnamestat": "NewStation",
            "shortnamestat": "NewShort",
            "longnamestat": "New Long Station Name",
            "starttimestat": "2023-09-07T03:20:11.078889Z",
            "latitudestat": 1.0,
            "longitudestat": 1.0,
            "altitudestat": 2000.0,
            "indstat": 2,
            "statestat": 2,
            "typestat": 3  # Este campo es opcional, ajusta según tu modelo
        }

        # Realiza una solicitud POST para crear un nuevo objeto de Station
        response = self.client.post(reverse("volcanoApp:station-list"), new_station_data, format="json")

        # Verifica que la respuesta sea un código 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verifica que el objeto de Station se ha creado correctamente en la base de datos
        self.assertEqual(Station.objects.count(), 2)  # Ajusta según sea necesario

    def test_read_station(self):
        # Realiza una solicitud GET para obtener la lista de objetos de Station
        response = self.client.get(reverse("volcanoApp:station-list"))

        # Verifica que la respuesta sea un código 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verifica que el objeto de Station creado en setUp está presente en la respuesta
        self.assertTrue(self.station.standardnamestat in str(response.data))

    def test_update_station(self):
        # Datos para actualizar el objeto de Station
        update_data = {
            "standardnamestat": "UpdatedStation",
            "shortnamestat": "UpdatedShort",
        }

        # Realiza una solicitud PATCH para actualizar el objeto de Station
        response = self.client.patch(reverse("volcanoApp:station-detail", args=[self.station.pk]), update_data, format="json")

        # Verifica que la respuesta sea un código 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Vuelve a obtener el objeto de Station desde la base de datos para verificar los cambios
        updated_station = Station.objects.get(pk=self.station.pk)

        # Verifica que los campos actualizados coincidan con los valores esperados
        self.assertEqual(updated_station.standardnamestat, "UpdatedStation")
        self.assertEqual(updated_station.shortnamestat, "UpdatedShort")
    def test_delete_station(self):
        # Realiza una solicitud DELETE para eliminar el objeto de Station
        response = self.client.delete(reverse("volcanoApp:station-detail", args=[self.station.pk]))

        # Verifica que la respuesta sea un código 204 No Content (indicando eliminación exitosa)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verifica que el objeto de Station se haya eliminado de la base de datos
        self.assertEqual(Station.objects.count(), 0)  # Ajusta según sea necesario
