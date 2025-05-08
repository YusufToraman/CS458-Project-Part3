import requests
from django.http import JsonResponse

GOOGLE_TOKEN_INFO_URL = "https://oauth2.googleapis.com/tokeninfo?id_token="

class GoogleService:

    @staticmethod
    def validate_token(id_token):
        try:
            google_response = requests.get(GOOGLE_TOKEN_INFO_URL + id_token)
            return google_response.json()
        except Exception:
            return None

    @staticmethod
    def is_token_valid(google_data):
        return "sub" in google_data
