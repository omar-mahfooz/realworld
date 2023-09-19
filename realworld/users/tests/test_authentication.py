"""
Tests for the user API.
"""

from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

from users.models import User

# class UserAuthenticationTestCase(APITestCase):
#     def setUp(self):
#         self.user_data = {
#                 "username": "Jacob",
#                 "email": "jake@jake.jake",
#                 "password": "jakejake"
#             }
#         self.user = User.objects.create_user(
#             username = self.user_data["username"],
#             email = self.user_data["email"],
#             password = self.user_data["password"]
#         )
        
        
        
#     def test_user_authentication(self):
#         authentication_data = {
#             "user": {
#                 "email": self.user_data["email"],
#                 "password": self.user_data["password"]
#             }
#         }
        
#         response = self.client.post(reverse('login'), authentication_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#         self.assertIn('user', response.data)

#         user = response.data['user']
#         self.assertEqual(user['email'], authentication_data['user']['email'])
#         self.assertEqual(user['username'], authentication_data['user']['username'])
#         self.assertEqual(user['bio'], '')
#         self.assertEqual(user['image'], '')
#         self.assertIn('token', user)
        

from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status
import pdb

class UserAuthenticationTestCase(APITestCase):
    def setUp(self):
        self.username = "Jacob"
        self.user_data = {
            "user": {
                "email": "jake@jake.jake",
                "password": "jakejake"
            }
        }
        self.user = User.objects.create_user(
            username="jake",
            email="jake@jake.jake",
            password="jakejake"
        )

    def test_user_login_success(self):
        pdb.set_trace()
        response = self.client.post(reverse('login'), self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['email'], self.user_data['user']['email'])
        # Add more assertions if needed for a successful login.

    def test_user_login_invalid_credentials(self):
        invalid_data = {
            "email": "jake@jake.jake",
            "password": "wrongpassword"
        }
        response = self.client.post(reverse('login'), invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Add assertions to check for an error message or response content.

    def test_user_login_missing_fields(self):
        incomplete_data = {
            "email": "jake@jake.jake",
        }
        response = self.client.post(reverse('login'), incomplete_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Add assertions to check for specific error messages or response content.

    # Add more test cases for edge cases or additional scenarios as needed.
