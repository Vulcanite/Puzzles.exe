from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class customuser(AbstractBaseUser, PermissionsMixin):
    user_role = (("1", "Employee"), ("2", "Helpdesk"))
    email = models.EmailField(_('email address'), primary_key=True,unique=True)
    firstname = models.CharField(max_length = 86)
    lastname = models.CharField(max_length = 106)
    role = models.CharField(default='1', choices=user_role, max_length=10) 
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname','lastname']

    objects = CustomUserManager()

    def __str__(self):
        return self.email