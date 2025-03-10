from django.db import models
from django.contrib.auth.models import User
from django.db.models.functions import Upper
from django.db.models.signals import post_save
from django.dispatch import receiver

from api.models.recipients import Recipient


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


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = UserProfile.objects.create(user=instance)
        recipient = Recipient.objects.create(
            type_id=user_profile.id, type=Recipient.PERSONAL
        )
        user_profile.recipient = recipient
        # user_profile.save(update_fields=["recipient"])

        # Subscription.objects.create(
        #     user_profile=user_profile, recipient=recipient, is_user_active=user_profile.is_active
        # )


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


class MarketingSubscriber(models.Model):
    email = models.EmailField(blank=False, db_index=True, unique=True)
