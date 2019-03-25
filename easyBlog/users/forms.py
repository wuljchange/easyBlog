from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label='邮件地址')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']