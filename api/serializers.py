from django.contrib.auth.models import User
from rest_framework import serializers


class MarketingSubscriberSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["email"]
