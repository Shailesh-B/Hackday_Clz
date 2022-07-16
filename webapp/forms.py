from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
USER = get_user_model()
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = USER
        fields = ('email', 'username',)
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = USER
        fields = ('email', 'username',)
