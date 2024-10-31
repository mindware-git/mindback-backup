from django.urls import path
from .views import marketing_subscriber, server_setting, UsersViewSet


users_list = UsersViewSet.as_view({"get": "list", "post": "create"})
user_detail = UsersViewSet.as_view({"get": "retrieve"})

urlpatterns = [
    path("v1/marketing/subscriptions", marketing_subscriber),
    path("v1/server_settings", server_setting),
    path("v1/users", users_list),
    path("v1/users/<str:email>", user_detail),
]
