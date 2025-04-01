import json
import os
import requests

from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.core.mail import send_mail as django_send_mail

from django.conf import settings

USERS_FILE = os.path.join(os.path.dirname(__file__), 'static_data/users.json')
GOOGLE_TOKEN_INFO_URL = "https://oauth2.googleapis.com/tokeninfo?id_token="
MAX_LOGIN_ATTEMPTS = 3
LOCKOUT_TIME = 10


def load_users_from_json():
    with open(USERS_FILE, 'r') as f:
        return json.load(f)


def save_users_to_json(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)


def is_valid_email(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


@api_view(['GET', 'POST'])
def send_email(request):
    data = request.data

    name = data.get('name')
    email = data.get('email')
    birthdate = data.get('birthdate')
    education = data.get('education')
    city = data.get('city')
    gender = data.get('gender')
    use_case = data.get('use_case')
    ai_models = data.get('ai_models', [])
    cons = data.get('cons', {})

    # Format email message
    models_with_cons = "\n".join([
        f"• {model}: {cons.get(model, 'No cons provided')}" for model in ai_models
    ])
    message = f"""
        📝 AI Survey Response

        👤 Name: {name}
        📧 Email: {email}
        🎂 Birthdate: {birthdate}
        🎓 Education: {education}
        🏙️ City: {city}
        ⚧️ Gender: {gender}

        🤖 AI Models Tried:
        {', '.join(ai_models)}

        ⚠️ Cons:
        {models_with_cons}

        ✅ Use Case:
        {use_case}
        """
    try:
        django_send_mail(
            "AI Survey Submission",
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        return JsonResponse({"message": "Email sent successfully"}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@api_view(['POST'])
def login_view(request):
    email = request.data.get("email")
    password = request.data.get("password")

    if email == "" or password == "":
        return JsonResponse({"error": "Email and password are required"}, status=400)

    if not is_valid_email(email):
        return JsonResponse({"error": "Invalid email format"}, status=400)

    failed_attempts = cache.get(f"failed_login_{email}", 0)
    if failed_attempts >= MAX_LOGIN_ATTEMPTS:
        return JsonResponse({"error": "Too many failed attempts. Try again later."}, status=403)

    users = load_users_from_json()

    user = next(
        (u for u in users if u["email"] == email and u["password"] == password), None)

    if user:
        cache.delete(f"failed_login_{email}")
        return JsonResponse({"message": "Successful Login", "user": f"{email}"}, status=200)

    cache.set(f"failed_login_{email}", failed_attempts + 1, LOCKOUT_TIME)
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

    users = load_users_from_json()

    for user in users:
        if user["email"] == email:
            if user["google_id"] is None:
                user["google_id"] = google_id
                save_users_to_json(users)
            return JsonResponse({"message": "Google Login Successful", "user": f"{email}"}, status=200)

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
