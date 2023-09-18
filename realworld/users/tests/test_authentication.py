"""
Tests for the user API.
"""

from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

class UserAuthenticationTestCase(APITestCase):
    def test_user_authentication(self):
        authentication_data = {
            "user": {
                "email": "jake@jake.jake",
                "password": "jakejake"
            }
        }
        
        response = self.client.post(reverse('login'), authentication_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

        self.assertIn('user', response.data)

        user = response.data['user']
        self.assertEqual(user['email'], authentication_data['user']['email'])
        self.assertEqual(user['username'], authentication_data['user']['username'])
        self.assertEqual(user['bio'], '')
        self.assertEqual(user['image'], '')
        self.assertIn('token', user)
        

