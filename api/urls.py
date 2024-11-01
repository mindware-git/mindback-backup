from django.urls import path, include
from .views import marketing_subscriber, server_setting, UserViewSet, MessageViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"messages", MessageViewSet, basename="message")


urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/marketing/subscriptions", marketing_subscriber),
    path("v1/server_settings", server_setting),
]
