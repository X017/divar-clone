from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
print("#[@] Started CustomUser")
class CustomUserManager(BaseUserManager):
    print('#[@] BaseUserManager started')
    def create_user(self, username, phone_number, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        if not phone_number:
            raise ValueError('The Phone Number field must be set')

        user = self.model(username=username, phone_number=phone_number, **extra_fields)
        user.set_password(password)  # Hashes the password
        user.save(using=self._db)
        return user

    def create_superuser(self, username, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        user = self.create_user(username, phone_number, password, **extra_fields)
        v= user.set_password(password)
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=11, unique=True)
    password = models.CharField(max_length=1000)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone_number']

    def __str__(self):
        return self.username
