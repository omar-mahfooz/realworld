"""
Tests for the user API.
"""

from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from users.models import User
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status



class UserAuthenticationTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Create data that should be shared among all test methods in the class
        
        cls.user_data = {"user": {"email": "jake@jake.jake", "password": "jakejake"}}
        cls.user = User.objects.create_user(
            username="jake", email="jake@jake.jake", password="jakejake"
        )

    @classmethod
    def tearDown(cls):
        # Clear the database after each test method
        User.objects.all().delete()

    def test_user_login_success(self):
        response = self.client.post(reverse("login"), self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["user"]["email"], self.user_data["user"]["email"]
        )
        # Add more assertions if needed for a successful login.

    def test_user_login_invalid_credentials(self):
        invalid_data = {
            "user": {"email": "jake@jake.jake", "password": "wrongpassword"}
        }
        
        response = self.client.post(reverse("login"), invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Add assertions to check for an error message or response content.

    def test_user_login_missing_fields(self):
        incomplete_data = {
            "email": "jake@jake.jake",
        }
        response = self.client.post(reverse("login"), incomplete_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Add assertions to check for specific error messages or response content.

    # Add more test cases for edge cases or additional scenarios as needed.
