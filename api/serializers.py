from rest_framework import serializers
from django.contrib.auth.models import User
from api.models.users import MarketingSubscriber


class MarketingSubscriberSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MarketingSubscriber
        fields = ["email"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
