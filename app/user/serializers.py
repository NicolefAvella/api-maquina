from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

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

    def update(Self, instance, validated_data):
        """Actualizacion usuario, pass corecta y devuelve esta"""
        password = validated_data.pop('password', None) #pop devuelve valor predeterminado
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user    

class AuthTokenSerializer(serializers.Serializer):
    """Serializer para la autenticacion usuario"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False  #es posible tener espacios en blanco en el pass
    )

    def validate(self, attrs):
        """Validacion y autenticacion usuario"""
        email = attrs.get('email') #obtenemos email
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:  #si la autenticacion falla aparece mensaje
            msg = _('No es posible autenticar con las credenciales ingresadas')
            raise serializers.ValidationError(msg, code='authorization') #se maneja como error 400

        attrs['user'] = user #busco user en los atributos para ser enviado al objeto usuario
        return attrs
