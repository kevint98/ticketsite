from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Ticket, User


class NewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'role', 'password1', 'password2']


class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = '__all__'
        exclude = ['owner', 'status', 'project_manager']
