'''from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from volcanoApp.models import Mask  # Importa el modelo desde la app correspondiente

class MaskCRUDTestCase(APITestCase):
    def setUp(self):
        # Crea un objeto Mask de ejemplo
        self.mask_data = {
            "idmask": "test_mask_id",
            "indmask": "A",
            "filenamemask": "test_mask.png",
            "directionmask": "test_direction",
            "heighmask": 100.0,
        }
        self.mask = Mask.objects.create(**self.mask_data)

    def test_create_mask(self):
        create_data = {
            "idmask": "new_mask_id",
            "indmask": "B",
            "filenamemask": "new_mask.png",
            "directionmask": "new_direction",
            "heighmask": 200.0,
        }
        response = self.client.post(reverse("volcanoApp:mask-create"), create_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verifica que el objeto se ha creado en la base de datos
        created_mask = Mask.objects.get(idmask="new_mask_id")
        self.assertEqual(created_mask.indmask, "B")

    def test_read_mask(self):
        response = self.client.get(reverse("volcanoApp:mask-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)  # Verifica que se devuelve al menos un objeto

    def test_update_mask(self):
        update_data = {
            "indmask": "C",
            "heighmask": 300.0,
        }
        response = self.client.patch(reverse("volcanoApp:mask-detail", args=[self.mask.idmask]), update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Vuelve a obtener el objeto de Mask desde la base de datos para verificar los cambios
        updated_mask = Mask.objects.get(idmask=self.mask.idmask)
        self.assertEqual(updated_mask.indmask, "C")
        self.assertEqual(updated_mask.heighmask, 300.0)

    def test_delete_mask(self):
        response = self.client.delete(reverse("volcanoApp:mask-detail", args=[self.mask.idmask]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verifica que el objeto se ha eliminado de la base de datos
        with self.assertRaises(Mask.DoesNotExist):
            Mask.objects.get(idmask=self.mask.idmask)
'''