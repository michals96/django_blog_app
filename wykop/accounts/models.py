from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    banned = models.BooleanField(default=False)
