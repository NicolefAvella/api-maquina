from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse  # para generar URL api

from rest_framework.test import APIClient
from rest_framework import status  # para los codigos estado ejem 200


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):  # podemos agregar varios argumentos
    """Helper function to create new user"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test de API usuario (public=no esta autenticado user)"""

    def setUp(self):
        self.client = APIClient() # cliente=APIcliente

    def test_create_valid_user_success(self):
        """Test creating using with a valid payload is successful"""
        payload = {
            'email': 'test@gmail.com',
            'password': 'testpass',
            'name': 'name',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(
            user.check_password(payload['password'])
        )
        self.assertNotIn('password', res.data)  # asegurar que la contraseña no se devuelva en el objeto

    def test_user_exists(self):
        """Test ccrear usuario que ya existe falla"""
        payload = {'email': 'test@gmail.com', 'password': 'testpass'}
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST) # espera 400 porque usuario ya existe

    def test_password_too_short(self):
        """Test that password must be more than 5 characters"""
        payload = {'email': 'test@gmail.com', 'password': 'pw'} # password menor 5 caracteres para prueba
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)  # esperamos que usuario no exista porque pass muy corta

    def test_create_token_for_user(self):
        """Test crea token para el usuario"""
        payload = {'email': 'test@gmail.com', 'password': 'testpass'}
        create_user(**payload)
        res = self.client.post(TOKEN_URL,payload)

        self.assertIn('token', res.data)  #espero respuesta 200 con token
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test token no se crea por credenciales no validas """
        create_user(email='test@gmail.com', password= 'testpass') #creo usuario
        payload = {'email': 'test@gmail.com', 'password': 'wrong'}   #cargamos dato erroneo
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)   #se espera token no exista
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_no_user(self):
        """Test token no se crea, usuario no existe"""
        payload = {'email': 'test@gmail.com', 'password': 'testpass'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test email y pass son requeridos"""
        res = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        
