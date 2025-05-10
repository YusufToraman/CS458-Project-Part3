from django.test import TestCase
from ..models import Survey, Question, QuestionOption
from django.core.exceptions import ValidationError
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

class TestQuestionView(TestCase):
    def test_create_survey_with_title(self):
        survey = Survey.objects.create(title="Test Survey")
        self.assertEqual(survey.title, "Test Survey")
        self.assertIsNotNone(survey.created_at)

    def test_all_question_types_allowed(self):
        types = ["multiple_choice", "rating", "text", "dropdown", "checkbox"]
        survey = Survey.objects.create(title="Test Survey")
        for t in types:
            q = Question.objects.create(
                survey=survey, question_text=f"Q ({t})", question_type=t)
            self.assertEqual(q.question_type, t)
        self.assertEqual(Question.objects.filter(
            survey=survey).count(), len(types))

    def test_create_conditional_question(self):
        survey = Survey.objects.create(title="Test Survey")
        q1 = Question.objects.create(
            survey=survey, question_text="Do you like ice cream?", question_type="dropdown")
        q2 = Question.objects.create(
            survey=survey,
            question_text="What flavor do you like?",
            question_type="dropdown",
            condition_question=q1,
            condition_answer="Yes"
        )
        self.assertEqual(q2.condition_question, q1)
        self.assertEqual(q2.condition_answer, "Yes")

    def test_create_multiple_choice_with_options(self):
        survey = Survey.objects.create(title="MC Survey")
        q = Question.objects.create(
            survey=survey, question_text="Pick a color", question_type="multiple_choice")
        o1 = QuestionOption.objects.create(question=q, text="Red")
        o2 = QuestionOption.objects.create(question=q, text="Blue")
    
        self.assertEqual(q.options.count(), 2)
        self.assertIn(o1, q.options.all())

    def test_create_checkbox_with_multiple_options(self):
        survey = Survey.objects.create(title="Hobby Survey")
        q = Question.objects.create(
            survey=survey, question_text="Choose hobbies", question_type="checkbox")
        hobbies = ["Reading", "Gaming", "Cooking"]
        for h in hobbies:
            QuestionOption.objects.create(question=q, text=h)
        self.assertEqual(q.options.count(), len(hobbies))

    def test_create_dropdown_with_options(self):
        survey = Survey.objects.create(title="Location Survey")
        q = Question.objects.create(
            survey=survey, question_text="Select your country", question_type="dropdown")
        QuestionOption.objects.create(question=q, text="USA")
        QuestionOption.objects.create(question=q, text="UK")
        self.assertEqual(q.options.count(), 2)

    def test_delete_survey_removes_questions_and_options(self):
        survey = Survey.objects.create(title="Cascade Test")
        q = Question.objects.create(
            survey=survey, question_text="Q1", question_type="checkbox")
        QuestionOption.objects.create(question=q, text="A")
        survey.delete()
        self.assertEqual(Question.objects.count(), 0)
        self.assertEqual(QuestionOption.objects.count(), 0)

    def test_create_question_with_empty_text_raises(self):
        survey = Survey.objects.create(title="Bad Q Test")
        with self.assertRaises(ValidationError):
            q = Question.objects.create(
                survey=survey, question_text="", question_type="text")
            q.full_clean()
            q.save()

    def test_invalid_question_type_raises(self):
        survey = Survey.objects.create(title="Bad Type Test")
        with self.assertRaises(ValidationError):
            q = Question(survey=survey, question_text="Invalid?",
                         question_type="not_a_type")
            q.full_clean()
            q.save()





class SubmitSurveyEndpointTests(APITestCase):
    def test_submit_full_survey(self):
        payload = {
            "title": "User Experience Survey",
            "questions": [
                {
                    "number": "1",
                    "question_text": "What is your age?",
                    "question_type": "text"
                },
                {
                    "number": "2",
                    "question_text": "Favorite languages?",
                    "question_type": "checkbox",
                    "options": [
                        {"text": "Python"},
                        {"text": "JavaScript"}
                    ]
                },
                {
                    "number": "3",
                    "question_text": "Do you like surveys?",
                    "question_type": "dropdown",
                    "options": [
                        {"text": "Yes"},
                        {"text": "No"}
                    ]
                }
            ]
        }

        response = self.client.post(
            reverse('survey_build'), data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_submit_survey_with_no_title(self):
        payload = {
            "title": "",
            "questions": [
                {
                    "number": "1",
                    "question_text": "aa",
                    "question_type": "text"
                }
            ]
        }

        response = self.client.post(
            reverse('survey_build'), data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_submit_survey_with_invalid_question_type(self):
        payload = {
            "title": "Invalid Type Survey",
            "questions": [
                {
                    "number": "1",
                    "question_text": "What is your age?",
                    "question_type": "invalid_type"
                }
            ]
        }

        response = self.client.post(
            reverse('survey_build'), data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_submit_survey_with_no_questions(self):
        payload = {
            "title": "No Questions Survey",
            "questions": []
        }

        response = self.client.post(
            reverse('survey_build'), data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_submit_survey_with_invalid_question_data(self):
        payload = {
            "title": "Invalid Question Data Survey",
            "questions": [
                {
                    "number": "1",
                    "question_text": "",
                    "question_type": "text"
                }
            ]
        }

        response = self.client.post(
            reverse('survey_build'), data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_submit_survey_with_multiple_choice_and_no_options(self):
        payload = {
            "title": "No Options Survey",
            "questions": [
                {
                    "number": "1",
                    "question_text": "Pick a color",
                    "question_type": "multiple_choice"
                }
            ]
        }

        response = self.client.post(
            reverse('survey_build'), data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_submit_survey_with_checkbox_and_no_options(self):
        payload = {
            "title": "No Options Survey",
            "questions": [
                {
                    "number": "1",
                    "question_text": "Pick a color",
                    "question_type": "checkbox"
                }
            ]
        }

        response = self.client.post(
            reverse('survey_build'), data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_submit_survey_with_dropdown_and_no_options(self):
        payload = {
            "title": "No Options Survey",
            "questions": [
                {
                    "number": "1",
                    "question_text": "Pick a color",
                    "question_type": "dropdown"
                }
            ]
        }

        response = self.client.post(
            reverse('survey_build'), data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_submit_survey_with_duplicate_question_text(self):
        payload = {
            "title": "Duplicate Question Survey",
            "questions": [
                {
                    "number": "1",
                    "question_text": "What is your age?",
                    "question_type": "text"
                },
                {
                    "number": "2",
                    "question_text": "What is your age?",
                    "question_type": "text"
                }
            ]
        }

        response = self.client.post(
            reverse('survey_build'), data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_submit_survey_with_duplicate_option_text(self):
        payload = {
            "title": "Duplicate Option Survey",
            "questions": [
                {
                    "number": "1",
                    "question_text": "Pick a color",
                    "question_type": "multiple_choice",
                    "options": [
                        {"text": "Red"},
                        {"text": "Red"}
                    ]
                }
            ]
        }

        response = self.client.post(
            reverse('survey_build'), data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_conditional_question(self):
        payload = {
            "title": "Conditional Survey",
            "questions": [
                {
                    "number": "1",
                    "question_text": "Do you like ice cream?",
                    "question_type": "dropdown",
                    "options": [{"text": "Yes"}, {"text": "No"}]
                },
                {
                    "number": "2",
                    "question_text": "What flavor?",
                    "question_type": "dropdown",
                    "condition_question": "1",
                    "condition_answer": "Yes",
                    "options": [{"text": "Vanilla"}, {"text": "Chocolate"}]
                }
            ]
        }
        res = self.client.post(reverse('survey_build'), data=payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_conditional_question_missing_answer(self):
        payload = {
            "title": "Missing Answer Condition",
            "questions": [
                {
                    "number": "1",
                    "question_text": "Do you like ice cream?",
                    "question_type": "dropdown",
                    "options": [{"text": "Yes"}, {"text": "No"}]
                },
                {
                    "number": "2",
                    "question_text": "What flavor?",
                    "question_type": "dropdown",
                    "condition_question": "1",
                    "condition_answer": "",
                    "options": [{"text": "Vanilla"}, {"text": "Chocolate"}]
                }
            ]
        }
        res = self.client.post(reverse('survey_build'), data=payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_condition_question_number(self):
        payload = {
            "title": "Invalid Condition Reference",
            "questions": [
                {
                    "number": "1",
                    "question_text": "Do you like ice cream?",
                    "question_type": "dropdown",
                    "options": [{"text": "Yes"}, {"text": "No"}]
                },
                {
                    "number": "2",
                    "question_text": "What flavor?",
                    "question_type": "dropdown",
                    "condition_question": "99",  # Invalid question number
                    "condition_answer": "Yes",
                    "options": [{"text": "Vanilla"}, {"text": "Chocolate"}]
                }
            ]
        }
        res = self.client.post(reverse('survey_build'), data=payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_circular_dependency(self):
        payload = {
            "title": "Circular Dependency",
            "questions": [
                {
                    "number": "1",
                    "question_text": "Do you like chocolate?",
                    "question_type": "dropdown",
                    "condition_question": "2",
                    "condition_answer": "Yes",
                    "options": [{"text": "Yes"}, {"text": "No"}]
                },
                {
                    "number": "2",
                    "question_text": "Do you like vanilla?",
                    "question_type": "dropdown",
                    "condition_question": 1,
                    "condition_answer": "Yes",
                    "options": [{"text": "Yes"}, {"text": "No"}]
                }
            ]
        }
        res = self.client.post(reverse('survey_build'), data=payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)