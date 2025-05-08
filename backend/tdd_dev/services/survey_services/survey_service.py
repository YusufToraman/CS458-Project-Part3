from collections import defaultdict
import uuid
from .validators import (
    EmailValidator, DateValidator, GenderValidator, AIModelValidator, 
    UseCaseValidator, RequiredFieldsValidator
)
from .email_service import EmailService
from .message_formatter import MessageFormatter
from django.http import JsonResponse

SEEN_EMAILS = set()

def reset_seen_emails():
    global SEEN_EMAILS
    SEEN_EMAILS.clear()

class SurveyService:
    def __init__(self):
        self.validators = [
            RequiredFieldsValidator(),
            DateValidator(),
            GenderValidator(),
            AIModelValidator(),
            UseCaseValidator(),
            EmailValidator()
        ]

    def validate(self, data):
        for validator in self.validators:
            error = validator.validate(data)
            if error:
                return JsonResponse({"error": error}, status=400)
        return None

    def submit_survey(self, data, request):
        # 1. Validasyon
        error = self.validate(data)
        if error:
            return error

        email = data["email"]

        # 2. Duplicate Kontrolü: Global email setine bak
        if email in SEEN_EMAILS:
            return JsonResponse({"error": "Duplicate survey submission"}, status=400)

        # 3. Yeni emaili kaydet
        SEEN_EMAILS.add(email)

        # 4. Mesajı oluştur ve gönder
        models_with_cons = "\n".join(
            f"• {model}: {data['cons'].get(model, 'No cons provided')}"
            for model in data["ai_models"]
        )
        message = MessageFormatter.format_message(data, models_with_cons)

        email_response = EmailService.send_email("AI Survey Submission", message, email)
        if "error" in email_response:
            return JsonResponse(email_response, status=500)

        # 5. Başarılı Yanıt
        return JsonResponse({"message": "Survey submitted successfully"}, status=200)