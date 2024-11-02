from django.test import TestCase
from django.contrib.auth.models import User

from rest_framework.test import APIClient

from api.models.recipients import Recipient


class MarketingSubscriptionsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_url(self):
        response = self.client.post(
            "/api/v1/marketing/subscriptions/",
            {"email": "test@test.com"},
            format="json",
        )
        self.assertEqual(response.status_code, 404)

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


class UserAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com"
        )

    def test_get_user_by_email_success(self):
        response = self.client.get(f"/api/v1/users/{self.user.email}/", format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["email"], self.user.email)

    def test_get_user_by_email_not_found(self):
        response = self.client.get(
            "/api/v1/users/nonexistent@example.com/", format="json"
        )
        self.assertEqual(response.status_code, 404)

    def test_other_methods_not_allowed(self):
        response = self.client.post(
            f"/api/v1/users/{self.user.email}/", data={}, format="json"
        )
        self.assertEqual(response.status_code, 405)

    def test_wrong_url(self):
        response = self.client.post(
            f"/api/v1/users/{self.user.email}", data={}, format="json"
        )
        self.assertEqual(response.status_code, 404)

    def test_create_user(self):
        response = self.client.post(
            "/api/v1/users/",
            {
                "email": "newuser@example.com",
                "password": "password123",
                "username": "newuser",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)

    def test_create_user_failure(self):
        response = self.client.post(
            "/api/v1/users/",
            {
                "email": "newuser@example.com",
                "password": "password123",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_user_creation_triggers_recipient_creation(self):
        response = self.client.post(
            "/api/v1/users/",
            {
                "email": "newuser@example.com",
                "password": "password123",
                "username": "newuser",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        user = User.objects.get(email="newuser@example.com")
        self.assertTrue(Recipient.objects.filter(type_id=user.userprofile.id).exists())
