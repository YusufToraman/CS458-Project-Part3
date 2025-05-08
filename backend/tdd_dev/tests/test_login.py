from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from unittest.mock import patch

class TestLoginView(TestCase):

    def test_empty_email_password(self):
        response = self.client.post(reverse('login'), {'email': '', 'password': ''})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Email and password are required", response.json().get("error"))

    def test_invalid_email_format(self):
        response = self.client.post(reverse('login'), {'email': 'invalidformat', 'password': '12345'})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid email format", response.json().get("error"))

    def test_successful_login(self):
        response = self.client.post(reverse('login'), {'email': 'admin@gmail.com', 'password': 'admin123'})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Successful Login", response.json().get("message"))

    def test_invalid_credentials(self):
        response = self.client.post(reverse('login'), {'email': 'wrong@gmail.com', 'password': 'wrongpass'})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid credentials", response.json().get("error"))

    def test_too_many_attempts(self):
        for _ in range(4):
            self.client.post(reverse('login'), {'email': 'admin@gmail.com', 'password': 'wrongpass'})
        response = self.client.post(reverse('login'), {'email': 'admin@gmail.com', 'password': 'wrongpass'})
        self.assertEqual(response.status_code, 403)
        self.assertIn("Too many failed attempts", response.json().get("error"))

    # Added after the initial test cases
    def test_sql_injection_protection(self):
        response = self.client.post(reverse('login'), {'email': 'test@example.com', 'password': "' OR 1=1 --"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid credentials", response.json().get("error"))

    @patch("requests.get")
    def test_google_login(self, mock_get):
        mock_get.return_value.json.return_value = {"sub": "101060969074824731216", "email": "yusuff.toramann@gmail.com"}
        
        response = self.client.post(reverse('google_login'), {'id_token': '101060969074824731216'})
        
        self.assertEqual(response.status_code, 200)
        self.assertIn("Google Login Successful", response.json().get("message", ""))

    def test_invalid_google_token(self):
        response = self.client.post(reverse('google_login'), {'id_token': 'invalid_token'})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid Google Token", response.json().get("error"))
