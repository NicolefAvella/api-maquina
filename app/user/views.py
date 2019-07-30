from rest_framework import generics

from user.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """Crea nuevo usuario en el sistemas"""
    serializer_class = UserSerializer
