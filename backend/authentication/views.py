from django.contrib.auth import login
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import CustomUser
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.decorators import api_view

import json
import os
from django.contrib.auth import login
from django.http import JsonResponse
from rest_framework.decorators import api_view

USERS_FILE = os.path.join(os.path.dirname(__file__), 'static_data/users.json')

def load_users():
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

@api_view(['POST'])
def login_view(request):
    email = request.data.get("email")
    password = request.data.get("password")
    users = load_users()

    user = next((u for u in users if u["email"] == email and u["password"] == password), None)

    if user:
        return JsonResponse({"message": "Successful Login"}, status=200)
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
