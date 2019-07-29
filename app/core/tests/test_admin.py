from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse # genera url para pagina admin
from django.test import Client # permite realizar solicitudes prueba


class AdminSiteTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@gmail.com',
            password='password123'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test@gmail.com',
            password='password123',
            name='Test User Full Name',
        )

    def test_users_listed(self):
        """Test usuario esta listado en pagina usuario"""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)   # realiza http get en la url

        self.assertContains(res, self.user.name) # se verifica si en res viene el name
        self.assertContains(res, self.user.email)

    def test_user_page_change(self):
        """Test pagina de edicion del usuario funciona"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200) # http 200 se refiere ok

    def test_create_user_page(self):
        """Crear pagina para login"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code,200)
