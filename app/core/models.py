from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin


class UserManager(BaseUserManager):  # creacion user, con las caracteristicas de BaseUser

    def create_user(self, email, password=None, **extra_fields):
        """Crear y guardar nuevo usuario"""
        if not email:
            raise ValueError('Se requiere email')
        user = self.model(email=self.normalize_email(email), **extra_fields) # normalize pasa a minuscula dominio del email
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self,email,password):
        """Crear y guardar superusuario"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    """Personaliza model, en vez de nombre usuario recibe correo"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email' # personalizamos para que en vez de nombre diga email
