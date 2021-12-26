import pytz
from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import timedelta, datetime

from django.conf import settings

class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='user', blank=True)
    age = models.PositiveSmallIntegerField(default=18, verbose_name='возраст')

    activation_key = models.CharField(max_length=128, blank=True, null=True)
    activation_key_expired = models.DateTimeField(blank=True, null=True)



    def is_activation_key_expired(self):
        if datetime.now(pytz.timezone(settings.TIME_ZONE)) <= self.activation_key_expired + timedelta(hours=48):
            return False
        return True
