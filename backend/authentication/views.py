from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required

import json
import os
import requests

import json
import os
import requests
from django.http import JsonResponse
from rest_framework.decorators import api_view

# Path to static JSON user storage
USERS_FILE = os.path.join(os.path.dirname(__file__), 'static_data/users.json')

# Load users from JSON
def load_users():
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

# Save users back to JSON
def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

# 🔹 Traditional Login (Email & Password)
@api_view(['POST'])
def login_view(request):
    email = request.data.get("email")
    password = request.data.get("password")
    users = load_users()

    user = next((u for u in users if u["email"] == email and u["password"] == password), None)

    if user:
        return JsonResponse({"message": "Successful Login"}, status=200)
    return JsonResponse({"error": "Invalid credentials"}, status=400)

# 🔹 Google Login (Verifies Google ID Token)
GOOGLE_TOKEN_INFO_URL = "https://oauth2.googleapis.com/tokeninfo?id_token="

@api_view(['POST'])
def google_login(request):
    id_token = request.data.get("id_token")  # Frontend sends this

    # Verify token with Google
    google_response = requests.get(GOOGLE_TOKEN_INFO_URL + id_token)
    google_data = google_response.json()

    if "sub" not in google_data:  # If 'sub' (Google ID) is missing, authentication failed
        return JsonResponse({"error": "Invalid Google Token"}, status=400)

    google_id = google_data["sub"]
    email = google_data["email"]

    users = load_users()

    for user in users:
        if user["email"] == email:
            if user["google_id"] is None:
                user["google_id"] = google_id  # Save Google ID
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
