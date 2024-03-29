from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag
from recipe import serializers

# Create your views here.

class TagViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Administarcion tags db"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

    def get_queryset(self):
        """Retorna objetos segun usuario autenticado"""
        return self.queryset.filter(user=self.request.user).order_by('-name')
