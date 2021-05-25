from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm

class CreateUserForm(UserCreationForm):
  class Meta:
    model = User
    fields = ['first_name', 'last_name', 'user_name', 'email', 'password1', 'password2', 'department', 'batch', 'phone', 'thumbnail']

class EditProfileForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ['first_name', 'last_name', 'user_name', 'email', 'department', 'batch', 'phone', 'thumbnail']