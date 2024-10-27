from django.urls import include, path
from .views import marketing_subscriber


# v1/users
# POST v1/users -> create user
# v1/messages
# POST v1/news/subscriptions -> subscribe
# DELETE v1/news/subscriptions -> unsubscribe

urlpatterns = [
    path("v1/marketing/subscriptions", marketing_subscriber),
]
