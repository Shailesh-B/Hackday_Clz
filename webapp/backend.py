import email
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
USER = get_user_model()


class EmailAuth(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = USER.objects.get(email=username)
        except USER.DoesNotExist:
            return None
        else:
            if getattr(user, "is_active", False) and user.check_password(password):
                return user
        return None

    def get_user(self, user_id):
        try:
            return USER.objects.get(pk=user_id)
        except USER.DoesNotExist:
            return None
