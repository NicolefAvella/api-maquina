from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag
from recipe.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')

class PublicTagApiTest(TestCase):
    """Test etiquetas disponibles"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test login necesario para recuperar tags"""
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateTagsApiTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
             'test@gmail.com',
             'password123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Test recuperar test"""
        Tag.objects.create(user=self.user, name='lore')
        Tag.objects.create(user=self.user, name='nico')

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):

        user2 = get_user_model().objects.create_user(
            'otro@gmail.com',
            'pass2',
        )
        Tag.objects.create(user=user2, name='cami')
        tag = Tag.objects.create(user=self.user, name='car')

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data),1)
        self.assertEqual(res.data[0]['name'], tag.name)
