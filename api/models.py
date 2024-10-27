from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class UserBaseSettings(models.Model):
    class Meta:
        abstract = True


class UserProfile(AbstractBaseUser, PermissionsMixin, UserBaseSettings):
    MAX_NAME_LENGTH = 100
    MIN_NAME_LENGTH = 2
