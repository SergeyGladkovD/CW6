from django.contrib.auth.forms import UserCreationForm

from mailing.forms import StyleMixin
from users.models import User


class UserRegisterForm(StyleMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "password1", "password2")


class UserManagerForm(StyleMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ("email", )
