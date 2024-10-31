from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db.models.functions import Upper
from django.utils.timezone import now as timezone_now


class UserBaseSettings(models.Model):
    class Meta:
        abstract = True


class UserProfile(AbstractBaseUser, PermissionsMixin, UserBaseSettings):
    USERNAME_FIELD = "email"
    MAX_NAME_LENGTH = 100
    MIN_NAME_LENGTH = 2
    API_KEY_LENGTH = 32
    NAME_INVALID_CHARS = ["*", "`", "\\", ">", '"', "@"]

    id = models.AutoField(
        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
    )
    email = models.EmailField(blank=False, db_index=True, unique=True)
    full_name = models.CharField(max_length=MAX_NAME_LENGTH)

    date_joined = models.DateTimeField(default=timezone_now)

    objects = UserManager()

    class Meta:
        indexes = [
            models.Index(Upper("email"), name="upper_userprofile_email_idx"),
        ]


class MarketingSubscriber(models.Model):
    email = models.EmailField(blank=False, db_index=True, unique=True)
