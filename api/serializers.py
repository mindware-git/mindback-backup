from rest_framework import serializers

from api.models.users import MarketingSubscriber, UserProfile


class MarketingSubscriberSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MarketingSubscriber
        fields = ["email"]


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"
