
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from volcanoApp.models import UserP
from volcanoApp.models import User

class RegistrationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse("volcanoApp:register") 
        self.login_url = reverse("volcanoApp:login") 
        self.logout_url = reverse("volcanoApp:logout")
        self.list_url = reverse("volcanoApp:userp-list")
        self.user = User.objects.create_user(
            username="testuserlogin",
            email="testuser@login.com", 
            password="testpassword",
            )

        """
        "institution= "SMT",
            coment= "aa coment test",
            phone = "+51977888666"
            """


    def test_successful_registration(self):
        data = {
            "names": "testuser",
            "lastname": "Test Lastname",
            "password": "testpassword",
            "email": "test@example.conm",
            "institution": "Test Institution",
            "comment": "Test Comment",
            "phone" : "+51977878666"
        }
        response = self.client.post(reverse("volcanoApp:register"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(UserP.objects.count(), 1)

    def test_missing_required_fields(self):
        data = {
            "names": "testuser",
            "lastname": "Test Lastname",
            # Missing 'password', 'email', and 'institution'
            "comment": "Test Comment"
        }
        response = self.client.post(reverse("volcanoApp:register"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(UserP.objects.count(), 0)

    def test_default_field_values(self):
        data = {
            "names": "testuser",
            "lastname": "Test Lastname",
            "password": "testpassword",
            "email": "test@exammple.cnom",
            "institution": "Test Institution",
            "comment": "Test Comment",
            "phone" : "+51677888666"
        }
        response = self.client.post(reverse("volcanoApp:register"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_profile = UserP.objects.first()
        self.assertEqual(user_profile.country, "")  # Empty country
        self.assertEqual(user_profile.city, "")     # Empty city
        self.assertEqual(user_profile.state, 1)     # State = 1
        self.assertIsNotNone(user_profile.datecreation)
        self.assertEqual(user_profile.type, 3)      # Type = 3

    def test_missing_optional_fields(self):
        data = {
            "names": "testuser",
            "lastname": "Test Lastname",
            "password": "testpassword",
            "email": "test@enxample.com",
            "institution": "Test Institution",
            "comment": "Test Comment",
            "phone" : "+51677888866"
            # Missing 'country', 'city', and 'state'
        }
        response = self.client.post(reverse("volcanoApp:register"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_profile = UserP.objects.first()
        self.assertEqual(user_profile.country, "")  # Empty country
        self.assertEqual(user_profile.city, "")     # Empty city
        self.assertEqual(user_profile.state, 1)     # State = 1

    def test_default_field_values_for_creation(self):
        data = {
            "names": "testuser",
            "lastname": "Test Lastname",
            "password": "testpassword",
            "email": "test@examnple.com",
            "institution": "Test Institution",
            "comment": "Test Comment",
            "state": 2  ,
            "phone" : "+51977888667"
        }
        response = self.client.post(reverse("volcanoApp:register"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_profile = UserP.objects.first()
        active = 1
        self.assertEqual(user_profile.state, active)     # State = 2 (overridden value)
#-----------------------------------------------------------------------------------------------------------login
    def test_successful_login(self):
        data = {
            "username": "testuserlogin",
            "password": "testpassword"
        }
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("token" in response.data)

    def test_invalid_credentials(self):
        data = {
            "username": "testuserlogin",
            "password": "incorrectpassword"
        }
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#-----------------------------------------------------------------------------------------------------------logout
    def test_successful_logout(self):
        # Iniciar sesión para obtener un token
        login_data = {
            "username": "testuserlogin",
            "password": "testpassword"
        }
        login_response = self.client.post(self.login_url, login_data, format="json")
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        token = login_response.data.get("token")

        # Realizar cierre de sesión con el token
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        response = self.client.post(self.logout_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_logout_without_authentication(self):
        # Intento de cierre de sesión sin autenticación
        response = self.client.post(self.logout_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#-----------------------------------------------------------------------------------------------------------lsitado edicion eliminar NO crear UserP
    def test_list_user_profiles(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_profile(self):
        user_profile = UserP.objects.create(
            id=self.user,
            names="testuserprof",
            lastname="Test Lastname",
            email="test@example.com",
            institution="Test Institution",
            comment="Test Comment",
            state=1,
            type=3
        )
        update_data = {
            "names": "updatedusername",
            "lastname": "Updated Lastname"
        }
        response = self.client.patch(reverse("volcanoApp:userp-detail", args=[self.user_profile.pk]), update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user_profile.names, "updatedusername")
        self.assertEqual(user_profile.lastname, "Updated Lastname")

    def test_update_user_profile(self):
        # Crear el perfil de usuario directamente en el test
        user_profile = UserP.objects.create(
            id=self.user,
            names="testuser",
            lastname="Test Lastname",
            email="test@example.com",
            institution="Test Institution",
            comment="Test Comment",
            state=1,
            type=3
        )

        update_data = {
            "names": "updatedusername",
            "lastname": "Updated Lastname"
        }
        response = self.client.patch(reverse("volcanoApp:userp-detail", args=[user_profile.pk])
                                     , update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_profile.refresh_from_db()
        self.assertEqual(user_profile.names, "updatedusername")
        self.assertEqual(user_profile.lastname, "Updated Lastname")

    def test_create_user_profile(self):
        # Intento de creación de un perfil de usuario, debería ser denegado
        create_data = {
            "names": "newuser",
            "lastname": "New Lastname",
            "email": "new@example.com",
            "institution": "New Institution",
            "comment": "New Comment",
            "state": 0,
            "type": 2
        }
        response = self.client.post(self.list_url, create_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(UserP.objects.filter(names="newuser").exists())

