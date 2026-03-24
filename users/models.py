from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True,
        verbose_name="Аватар",
    )
    bio = models.TextField(
        blank=True,
        verbose_name="О себе",
    )