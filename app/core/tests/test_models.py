from django.test import TestCase
from django.contrib.auth import get_user_model
"""Test para models """

class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test verifica user se haya creado correcto con email"""
        email = 'test@gmail.com' # dato prueba
        password = 'Password123'        # dato prueba
        user = get_user_model().objects.create_user(
			email=email,
			password=password
		) # llama a la funcion para crear usuario

        self.assertEqual(user.email, email) # asercion para verificar email=email creado
        self.assertTrue(user.check_password(password)) # verifica password devuelve true or false

    def test_new_user_email_normalized(self):
	    """Test email para que pase a minuscula lo que sigue despues de @"""
	    email = 'test@GMAIL.com'
	    user = get_user_model().objects.create_user(email, 'test123')

	    self.assertEqual(user.email, email.lower())  # convierte dominio en minuscula

    def test_new_user_invalid_email(self):
        """Test error por crear usuario sin email"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """Test crear super usuario"""
        user = get_user_model().objects.create_superuser(
               'test@gmail.com',
               'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
