from typing import Any, Dict, Mapping, Optional, Type, Union
from django.contrib.auth.forms import UserCreationForm
from django.core.files.base import File
from django.db.models.base import Model
from django.forms import ModelForm, HiddenInput
from django.forms.utils import ErrorList
from .models import Ticket, User


class NewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'role', 'password1', 'password2']


class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = '__all__'
        exclude = ['owner', 'project_manager']

    def __init__(self, *args, **kwargs):
        is_project_manager = kwargs.get('is_project_manager', False)
        if 'is_project_manager' in kwargs:
            del kwargs['is_project_manager']
        super().__init__(*args, **kwargs)
        if not is_project_manager:
            self.fields['status'].widget = HiddenInput()
