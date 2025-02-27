from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework.decorators import api_view
import json
import os
import requests

USERS_FILE = os.path.join(os.path.dirname(__file__), 'static_data/users.json')
GOOGLE_TOKEN_INFO_URL = "https://oauth2.googleapis.com/tokeninfo?id_token="


def load_users():
    with open(USERS_FILE, 'r') as f:
        return json.load(f)


def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)


@api_view(['POST'])
def login_view(request):
    email = request.data.get("email")
    password = request.data.get("password")
    users = load_users()

    user = next(
        (u for u in users if u["email"] == email and u["password"] == password), None)

    if user:
        return JsonResponse({"message": "Successful Login"}, status=200)
    return JsonResponse({"error": "Invalid credentials"}, status=400)


@api_view(['POST'])
def google_login(request):
    id_token = request.data.get("id_token")

    google_response = requests.get(GOOGLE_TOKEN_INFO_URL + id_token)
    google_data = google_response.json()

    if "sub" not in google_data:
        return JsonResponse({"error": "Invalid Google Token"}, status=400)

    google_id = google_data["sub"]
    email = google_data["email"]

    users = load_users()

    for user in users:
        if user["email"] == email:
            if user["google_id"] is None:
                user["google_id"] = google_id
                save_users(users)
            return JsonResponse({"message": "Google Login Successful"}, status=200)

    return JsonResponse({"error": "User not found"}, status=404)


@login_required
def get_user_profile(request):
    user = request.user
    return JsonResponse({
        "username": user.username,
        "email": user.email,
        "google_id": user.google_id,
        "profile_picture": user.profile_picture
    })
