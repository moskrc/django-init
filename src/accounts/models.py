import logging
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone
from django_extensions.db.fields import UUIDField

log = logging.getLogger('project')

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password, site, **extra_fields):
        now = timezone.now()
        user = self.model(username=username, email=email,
                          is_staff=False, is_active=True, is_superuser=False,
                          last_login=now, date_joined=now, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        u = self.create_user(username, email, password, None, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u


class User(AbstractUser):
    uuid = UUIDField(verbose_name='uuid')
    title = models.CharField(max_length=255, blank=True)
    avatar = models.ImageField(upload_to='avatars', blank=True, null=True)

    USERNAME_FIELD = 'username'

    objects = CustomUserManager()
