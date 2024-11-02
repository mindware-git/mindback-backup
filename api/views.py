from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from api.models.messages import Message

from .serializers import MarketingSubscriberSerializer, UserSerializer


@api_view(["POST"])
def marketing_subscriber(request):
    if request.method == "POST":
        serializer = MarketingSubscriberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def server_setting(request):
    return Response({"server_version": "0.0.1"}, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "email"
    lookup_value_regex = "[\w@.]+"


class MessageViewSet(viewsets.ModelViewSet):
    # serializer_class = MessageSerializer
    queryset = Message.objects.all()
