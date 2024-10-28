from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models.functions import Upper


# class UserBaseSettings(models.Model):
#     class Meta:
#         abstract = True


# class UserProfile(AbstractBaseUser, PermissionsMixin, UserBaseSettings):
#     MAX_NAME_LENGTH = 100
#     MIN_NAME_LENGTH = 2
#     id = models.AutoField(
#         auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
#     )
#     email = models.EmailField(blank=False, db_index=True)

#     class Meta:
#         indexes = [
#             models.Index(Upper("email"), name="upper_userprofile_email_idx"),
#         ]


class MarketingSubscriber(models.Model):
    email = models.EmailField(blank=False, db_index=True, unique=True)
