from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from volcanoApp.models import Mask,Station, Volcano, Imagesegmentation  # Importa el modelo desde la app correspondiente

class MaskCRUDTestCase(APITestCase):
    def setUp(self):
        self.station = Station.objects.create(
            idstation="STAT",
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
        self.image_segmentation = Imagesegmentation.objects.create(
            #VVVSSSSYYYYMMDDhhmmss
            idphoto='SABSABA20231111040400',
            urlimg='URL of Image',
            filenameimg='Filename.jpg',
            stateimg=1,  # Tu valor para stateimg
            idstation=self.station  # Usar la instancia de Station creada arriba
        )
        self.mask = Mask.objects.create(
            idmask = self.image_segmentation,
            indmask= 1,
            starttimemask="2023-09-06T03:20:11.078889Z",
            filenamemask= "test_mask.png",
            directionmask = "test_direction",
            heighmask= 100.0,
            statemask= 1
        )

    def test_create_mask(self):
        image_segmentationc = Imagesegmentation.objects.create(
            #VVVSSSSYYYYMMDDhhmmss
            idphoto='SABSABA20231111040403',
            urlimg='URL of Image',
            filenameimg='Filename.jpg',
            stateimg=1,  # Tu valor para stateimg
            idstation=self.station  # Usar la instancia de Station creada arriba
        )
        create_data = {
            "idmask": image_segmentationc.idphoto,
            "indmask": 1,
            "filenamemask": "new_mask.png",
            "directionmask": "new_direction",
            "starttimemask":"2023-09-06T03:20:11.078889Z",
            "heighmask": 200.0,
            "statemask": 1
        }
        response = self.client.post(reverse("volcanoApp:mask-list"), create_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verifica que el objeto se ha creado en la base de datos
        created_mask = Mask.objects.get(idmask="SABSABA20231111040400")
        self.assertEqual(created_mask.indmask, 1)

    def test_read_mask(self):
        response = self.client.get(reverse("volcanoApp:mask-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)  # Verifica que se devuelve al menos un objeto

    def test_update_mask(self):
        update_data = {
            "indmask": 1,
            "heighmask": 300.0,
        }
        response = self.client.patch(reverse("volcanoApp:mask-detail", args=[self.mask.pk]), update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Vuelve a obtener el objeto de Mask desde la base de datos para verificar los cambios
        updated_mask = Mask.objects.get(idmask=self.mask.idmask)
        self.assertEqual(updated_mask.indmask, 1)
        self.assertEqual(updated_mask.heighmask, 300.0)

    def test_delete_mask(self):
        response = self.client.delete(reverse("volcanoApp:mask-detail", args=[self.mask.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verifica que el objeto se ha eliminado de la base de datos
        with self.assertRaises(Mask.DoesNotExist):
            Mask.objects.get(idmask=self.mask.idmask)
