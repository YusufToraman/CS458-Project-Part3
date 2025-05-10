from django.http import JsonResponse
from rest_framework.decorators import api_view
from .services.login_services.user_service import UserService
from .services.login_services.google_service import GoogleService
from .services.survey_services.survey_service import SurveyService
from rest_framework.response import Response
from rest_framework import status
from .models import Survey, Question, QuestionOption

@api_view(['POST'])
def login_view(request):
    email = request.data.get("email", "")
    password = request.data.get("password", "")

    if not email or not password:
        return JsonResponse({"error": "Email and password are required"}, status=400)

    if not UserService.is_valid_email(email):
        return JsonResponse({"error": "Invalid email format"}, status=400)

    if UserService.is_account_locked(email):
        return JsonResponse({"error": "Too many failed attempts"}, status=403)

    user = UserService.find_user_by_email(email)
    if not user or user.get("password") != password:
        UserService.update_failed_attempts(email)
        return JsonResponse({"error": "Invalid credentials"}, status=400)

    UserService.reset_failed_attempts(email)
    return JsonResponse({"message": "Successful Login", "user": email}, status=200)

@api_view(['POST'])
def google_login(request):
    id_token = request.data.get("id_token")

    google_data = GoogleService.validate_token(id_token)
    if not google_data or not GoogleService.is_token_valid(google_data):
        return JsonResponse({"error": "Invalid Google Token"}, status=400)

    google_id = google_data["sub"]
    email = google_data["email"]

    user = UserService.find_user_by_email(email)
    if user:
        if user.get("google_id") != google_id:
            user["google_id"] = google_id
            users = UserService.load_users()
            UserService.save_users(users)
        return JsonResponse({"message": "Google Login Successful", "user": email}, status=200)

    return JsonResponse({"error": "User not found"}, status=404)

@api_view(['POST'])
def submit_survey(request):
    survey_service = SurveyService()
    data = request.data
    return survey_service.submit_survey(data, request)


@api_view(['POST'])
def survey_build(request):
    data = request.data
    title = data.get("title")
    questions = data.get("questions", [])

    VALID_TYPES = {"text", "multiple_choice", "dropdown", "checkbox", "rating"}

    if not title or not isinstance(title, str) or title.strip() == "":
        return Response({"error": "Title is required."}, status=status.HTTP_400_BAD_REQUEST)

    if not questions or not isinstance(questions, list) or len(questions) == 0:
        return Response({"error": "At least one valid question is required."}, status=status.HTTP_400_BAD_REQUEST)

    seen_texts = set()
    uuid_to_question_data = {}

    for q in questions:
        number = q.get("number") 
        question_text = q.get("question_text", "").strip()
        question_type = q.get("question_type")
        condition_question = q.get("condition_question")
        condition_answer = q.get("condition_answer", "").strip()

        if not number or not isinstance(number, str):
            return Response({"error": "Each question must have a unique string 'number' identifier (UUID)."}, status=status.HTTP_400_BAD_REQUEST)

        if question_type not in VALID_TYPES or question_text == "":
            return Response({"error": f"Invalid data in question with UUID {number}."}, status=status.HTTP_400_BAD_REQUEST)

        if question_text in seen_texts:
            return Response({"error": f"Duplicate question text: '{question_text}'."}, status=status.HTTP_400_BAD_REQUEST)
        seen_texts.add(question_text)

        if question_type in {"multiple_choice", "dropdown", "checkbox"}:
            options = q.get("options", [])
            if not isinstance(options, list) or not options:
                return Response({"error": f"Options required for question '{question_text}'."}, status=status.HTTP_400_BAD_REQUEST)

            option_texts = set()
            for opt in options:
                text = opt.get("text", "").strip()
                if not text:
                    return Response({"error": f"Empty option in question '{question_text}'."}, status=status.HTTP_400_BAD_REQUEST)
                if text in option_texts:
                    return Response({"error": f"Duplicate option text '{text}' in question '{question_text}'."}, status=status.HTTP_400_BAD_REQUEST)
                option_texts.add(text)

        if condition_question:
            if condition_question == number:
                return Response({"error": f"Question {number} cannot depend on itself."}, status=status.HTTP_400_BAD_REQUEST)
            if not any(q2.get("number") == condition_question for q2 in questions):
                return Response({"error": f"Invalid condition_question reference: {condition_question}"}, status=status.HTTP_400_BAD_REQUEST)
            if not condition_answer:
                return Response({"error": f"Missing condition_answer for question '{question_text}'."}, status=status.HTTP_400_BAD_REQUEST)

        uuid_to_question_data[number] = q

    for q in questions:
        number = q.get("number")
        cond = q.get("condition_question")
        if cond:
            other = uuid_to_question_data.get(cond)
            if other and other.get("condition_question") == number:
                return Response({"error": f"Circular dependency between questions '{number}' and '{cond}'."}, status=status.HTTP_400_BAD_REQUEST)

    survey = Survey.objects.create(title=title.strip())
    uuid_to_instance = {}

    for q in questions:
        question = Question.objects.create(
            survey=survey,
            question_text=q["question_text"].strip(),
            question_type=q["question_type"]
        )
        uuid_to_instance[q["number"]] = question

    for q in questions:
        question = uuid_to_instance[q["number"]]
        cond_uuid = q.get("condition_question")

        if cond_uuid:
            question.condition_question = uuid_to_instance.get(cond_uuid)
            question.condition_answer = q.get("condition_answer", "").strip()
            question.save()

        if question.question_type in {"multiple_choice", "dropdown", "checkbox"}:
            for opt in q.get("options", []):
                text = opt.get("text", "").strip()
                if text:
                    QuestionOption.objects.create(question=question, text=text)

    return Response(
        {"message": "Survey saved successfully", "survey_id": survey.id},
        status=status.HTTP_201_CREATED
    )
