from django.test import TestCase
from rest_framework.test import APIClient
from .models import MarketingSubscriber


class MarketingSubscriptionsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_already_exist(self):
        response = self.client.post(
            "/api/v1/marketing/subscriptions", {"email": "test@test.com"}, format="json"
        )
        self.assertEqual(response.status_code, 201)
        response = self.client.post(
            "/api/v1/marketing/subscriptions", {"email": "test@test.com"}, format="json"
        )
        self.assertEqual(response.status_code, 400)

    def test_invalid_email(self):
        response = self.client.post(
            "/api/v1/marketing/subscriptions", {"email": "test"}, format="json"
        )
        self.assertEqual(response.status_code, 400)
