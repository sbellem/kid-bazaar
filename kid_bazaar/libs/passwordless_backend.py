from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class PasswordlessAuthBackend(ModelBackend):
    """Log in to Django without providing a password.

    """
    def authenticate(self, email=None):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None