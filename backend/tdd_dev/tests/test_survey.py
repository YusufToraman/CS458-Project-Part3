from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from ..services.survey_services.survey_service import reset_seen_emails

class TestSurveySubmission(TestCase):

    def setUp(self):
        reset_seen_emails()

    def test_empty_form_submission(self):
        """Test if the survey form is submitted empty"""
        response = self.client.post(reverse('submit_survey'))
        self.assertEqual(response.status_code, 400)
        self.assertIn("All fields are required", response.json().get("error"))

    def test_invalid_email_format(self):
        """Test for invalid email format"""
        data = {
            "email": "invalidemail",
            "name": "Yusuf Toraman",
            "birthdate": "01/01/2000",
            "education": "Bachelors",
            "city": "Istanbul",
            "gender": "Male",
            "ai_models": ["ChatGPT"],
            "cons": {"ChatGPT": "Sometimes inaccurate"},
            "use_case": "Writing code"
        }
        response = self.client.post(reverse('submit_survey'), data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid email format", response.json().get("error"))

    def test_invalid_date_format(self):
        """Test for invalid date format"""
        data = {
            "email": "example@gmail.com",
            "name": "Burak Demirel",
            "birthdate": "2000/01/01",
            "education": "High School",
            "city": "Istanbul",
            "gender": "Male",
            "ai_models": ["ChatGPT"],
            "cons": {"ChatGPT": "Sometimes inaccurate"},
            "use_case": "Writing code"
        }
        response = self.client.post(reverse('submit_survey'), data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid date format", response.json().get("error"))

    def test_invalid_gender(self):
        """Test submission with an invalid gender"""
        data = {
            "email": "example@gmail.com",
            "name": "Kaan Oktay",
            "birthdate": "01/01/2000",
            "education": "Masters",
            "city": "Istanbul",
            "gender": "Unknown",
            "ai_models": ["ChatGPT"],
            "cons": {"ChatGPT": "Sometimes inaccurate"},
            "use_case": "Writing code"
        }
        response = self.client.post(reverse('submit_survey'), data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid gender", response.json().get("error"))

    def test_successful_survey_submission(self):
        data = {
            "email": "example@gmail.com",
            "name": "Yusuf Toraman",
            "birthdate": "01/01/2000",
            "education": "High School",
            "city": "Istanbul",
            "gender": "Male",
            "ai_models": ["ChatGPT", "Bard"],
            "cons": {"ChatGPT": "Sometimes inaccurate", "Bard": "Slow responses"},
            "use_case": "Writing code"
        }
        response = self.client.post(reverse('submit_survey'), data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Survey submitted successfully", response.json().get("message"))

    def test_missing_required_field(self):
        """Test submission with a missing required field (name)"""
        data = {
            "email": "example@gmail.com",
            "birthdate": "01/01/2000",
            "education": "PhD",
            "city": "Istanbul",
            "gender": "Male",
            "ai_models": ["ChatGPT"],
            "cons": {"ChatGPT": "Sometimes inaccurate"},
            "use_case": "Writing code"
        }
        response = self.client.post(reverse('submit_survey'), data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn("All fields are required", response.json().get("error"))

    def test_duplicate_submission(self):
        """Test multiple survey submissions from the same email"""
        data = {
            "email": "example@gmail.com",
            "name": "Dilara Mandıracı",
            "birthdate": "01/01/2000",
            "education": "High School",
            "city": "Istanbul",
            "gender": "Male",
            "ai_models": ["ChatGPT"],
            "cons": {"ChatGPT": "Sometimes inaccurate"},
            "use_case": "Writing code"
        }
        response1 = self.client.post(reverse('submit_survey'), data, content_type='application/json')
        self.assertEqual(response1.status_code, 200)
        self.assertIn("Survey submitted successfully", response1.json().get("message"))

        response2 = self.client.post(reverse('submit_survey'), data, content_type='application/json')
        self.assertEqual(response2.status_code, 400)
        self.assertIn("Duplicate survey submission", response2.json().get("error"))

    def test_all_ai_models_selected(self):
        """Test submission with all AI models selected"""
        data = {
            "email": "example@gmail.com",
            "name": "Burak Demirel",
            "birthdate": "01/01/2000",
            "education": "Bachelors",
            "city": "Istanbul",
            "gender": "Male",
            "ai_models": ["ChatGPT", "Bard", "Claude", "Copilot"],
            "cons": {
                "ChatGPT": "Sometimes inaccurate",
                "Bard": "Slow responses",
                "Claude": "Limited knowledge",
                "Copilot": "Code errors"
            },
            "use_case": "Writing code"
        }
        response = self.client.post(reverse('submit_survey'), data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Survey submitted successfully", response.json().get("message"))

    def test_empty_use_case(self):
        """Test submission with an empty use case"""
        data = {
            "email": "example@gmail.com",
            "name": "Yusuf Toraman",
            "birthdate": "01/01/2000",
            "education": "Bachelors",
            "city": "Istanbul",
            "gender": "Male",
            "ai_models": ["ChatGPT"],
            "cons": {"ChatGPT": "Sometimes inaccurate"},
            "use_case": ""
        }
        response = self.client.post(reverse('submit_survey'), data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn("All fields are required", response.json().get("error"))


    def test_successful_email_sent(self):
        """Test if the email is sent after successful submission"""
        data = {
            "email": "example@gmail.com",
            "name": "Dilara Mandıracı",
            "birthdate": "01/01/2000",
            "education": "Bachelors",
            "city": "Istanbul",
            "gender": "Male",
            "ai_models": ["ChatGPT"],
            "cons": {"ChatGPT": "Sometimes inaccurate"},
            "use_case": "Writing code"
        }
        response = self.client.post(reverse('submit_survey'), data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Survey submitted successfully", response.json().get("message"))
