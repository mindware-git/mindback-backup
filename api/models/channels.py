from django.db import models


class Channel(models.Model):
    MAX_NAME_LENGTH = 60
    MAX_DESCRIPTION_LENGTH = 1024
