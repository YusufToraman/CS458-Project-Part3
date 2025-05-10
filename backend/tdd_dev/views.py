from django.http import JsonResponse
from rest_framework.decorators import api_view
from .services.login_services.user_service import UserService
from .services.login_services.google_service import GoogleService
from .services.survey_services.survey_service import SurveyService
from rest_framework.response import Response
from rest_framework import status
from .models import Survey, Question, QuestionOption
from .serializers import SurveyBuildSerializer

from rest_framework.exceptions import ValidationError
from .services.question_services.survey_builder import SurveyBuilder


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
    serializer = SurveyBuildSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        builder = SurveyBuilder(serializer.validated_data)
        builder.validate_business_rules()
        survey = builder.build()
    except ValidationError as e:
        return Response({"error": str(e.detail if hasattr(e, "detail") else e)}, status=status.HTTP_400_BAD_REQUEST)

    return Response(
        {"message": "Survey saved successfully", "survey_id": survey.id},
        status=status.HTTP_201_CREATED
    )
