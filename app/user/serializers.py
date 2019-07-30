from django.contrib.auth import get_user_model

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializador para el objeto usuario"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')  #campos deseo incluir convertir a json
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}  #test 5 caracteres minimo pass, establece restricciones

    def create(self, validated_data):
        """Crear nuevo usuario con pass encriptada y retornarlo"""
        return get_user_model().objects.create_user(**validated_data) #llamo a funcion en modelo
