from django.contrib.auth.forms import UserCreationForm
from .models import User


class NewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'password1', 'password2']
