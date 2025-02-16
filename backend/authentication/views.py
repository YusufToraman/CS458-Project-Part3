from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import CustomUser
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from allauth.socialaccount.models import SocialAccount
from rest_framework.decorators import api_view

@api_view(['POST'])
def login_view(request):
    email = request.data.get("email")
    password = request.data.get("password")
    user = authenticate(request, username=email, password=password)

    if user:
        login(request, user)
        return JsonResponse({"message": "Succesfull Login"}, status=200)
    else:
        return JsonResponse({"error": "Invalid credentials"}, status=400)


@api_view(['POST'])
def google_login(request):
    google_id = request.data.get("google_id")
    try:
        user = CustomUser.objects.get(google_id=google_id)
        login(request, user)
        return Response({"message": "Google Login Successful"}, status=200)
    except CustomUser.DoesNotExist:
        return Response({"error": "User not found"}, status=404)


@login_required
def get_user_profile(request):
    user = request.user
    return JsonResponse({
        "username": user.username,
        "email": user.email,
        "google_id": user.google_id,
        "profile_picture": user.profile_picture
    })
