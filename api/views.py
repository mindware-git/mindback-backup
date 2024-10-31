from rest_framework import viewsets
from .serializers import MarketingSubscriberSerializer, UserProfileSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import UserProfile


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
    return Response({"server_version": "0.0.1"})


class UsersViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
