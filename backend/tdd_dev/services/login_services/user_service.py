import os
import json
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

USERS_FILE = os.path.join(os.path.dirname(__file__), '../../static_data/users.json')
MAX_LOGIN_ATTEMPTS = 3
LOCKOUT_TIME = 10

class UserService:

    @staticmethod
    def load_users():
        with open(USERS_FILE, 'r') as f:
            return json.load(f)

    @staticmethod
    def save_users(users):
        with open(USERS_FILE, 'w') as f:
            json.dump(users, f, indent=4)

    @staticmethod
    def is_valid_email(email):
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False

    @staticmethod
    def find_user_by_email(email):
        users = UserService.load_users()
        return next((u for u in users if u["email"] == email), None)

    @staticmethod
    def update_failed_attempts(email):
        failed_attempts = cache.get(f"failed_login_{email}", 0) + 1
        cache.set(f"failed_login_{email}", failed_attempts, LOCKOUT_TIME)

    @staticmethod
    def reset_failed_attempts(email):
        cache.delete(f"failed_login_{email}")

    @staticmethod
    def is_account_locked(email):
        return cache.get(f"failed_login_{email}", 0) >= MAX_LOGIN_ATTEMPTS
