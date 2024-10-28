from rest_framework import serializers
from .models import MarketingSubscriber


class MarketingSubscriberSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MarketingSubscriber
        fields = ["email"]
