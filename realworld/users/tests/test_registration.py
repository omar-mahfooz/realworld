"""
Tests for the user API.
"""

from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

class UserRegistrationTestCase(APITestCase):
    def test_user_registration(self):
        registration_data = {
            "user": {
                "username": "Jacob",
                "email": "jake@jake.jake",
                "password": "jakejake"
            }
        }
        
        response = self.client.post(reverse('registration'), registration_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertIn('user', response.data)

        user = response.data['user']
        self.assertEqual(user['email'], registration_data['user']['email'])
        self.assertEqual(user['username'], registration_data['user']['username'])
        self.assertEqual(user['bio'], '')
        self.assertEqual(user['image'], '')
        self.assertIn('token', user)
        
        # Add more assertions to test the response data, if needed.

