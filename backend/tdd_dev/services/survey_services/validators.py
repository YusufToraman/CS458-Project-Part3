from datetime import datetime
import re

class BaseValidator:
    def validate(self, data: dict) -> str | None:
        raise NotImplementedError


class RequiredFieldsValidator(BaseValidator):
    _required = {
        "name", "email", "birthdate", "education",
        "city", "gender", "use_case", "ai_models",
    }

    def validate(self, data):
        for field in self._required:
            if not data.get(field):
                return "All fields are required"
        return None


class EmailValidator(BaseValidator):
    _regex = re.compile(r"^[^@]+@[^@]+\.[^@]+$")

    def validate(self, data):
        email = data.get("email", "")
        if not isinstance(email, str) or not self._regex.match(email):
            return "Invalid email format"
        return None


class DateValidator(BaseValidator):
    def validate(self, data):
        birthdate = data.get("birthdate", "")
        if not isinstance(birthdate, str):
            return "Invalid date format"
        try:
            datetime.strptime(birthdate, "%d/%m/%Y")
        except ValueError:
            return "Invalid date format"
        return None


class GenderValidator(BaseValidator):
    _allowed = {"Male", "Female"}

    def validate(self, data):
        gender = data.get("gender")
        if gender not in self._allowed:
            return "Invalid gender"
        return None


class AIModelValidator(BaseValidator):
    def validate(self, data):
        models = data.get("ai_models")
        if not isinstance(models, list) or len(models) == 0:
            return "At least one AI model must be selected"
        return None


class UseCaseValidator(BaseValidator):
    def validate(self, data):
        use_case = data.get("use_case", "")
        if not isinstance(use_case, str) or not use_case.strip():
            return "Use case is required"
        return None
