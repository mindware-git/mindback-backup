from rest_framework import viewsets
from .serializers import MarketingSubscriberSerializer
from rest_framework.decorators import api_view


@api_view(["POST", "DELETE"])
def marketing_subscriber(request):
    if request.method == "POST":
        # serializer =
        return Response(serializer.data)
    elif request.method == "DELETE":
        # subscriber = MarketingSubscriberSerializer.objects.?
        subscriber.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
