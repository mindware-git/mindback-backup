from django.db import models
from django.contrib.auth.models import User
from django.db.models.functions import Upper
from django.utils.timezone import now as timezone_now

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.AutoField(
        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
    )
    is_bot = models.BooleanField(default=False, db_index=True)
    bot_type = models.PositiveSmallIntegerField(null=True, db_index=True)
    # bot_owner = models.ForeignKey("self", null=True, on_delete=models.SET_NULL)

#     class Meta:
#         indexes = [
#             models.Index(Upper("email"), name="upper_userprofile_email_idx"),
#         ]


class MarketingSubscriber(models.Model):
    email = models.EmailField(blank=False, db_index=True, unique=True)
