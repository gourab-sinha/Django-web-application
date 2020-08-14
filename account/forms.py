from django import forms
from django.contrib.auth.forms import UserCreationForm
from account.models import Account


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(help_text="Required. Add a valid email address.")

    class Meta:
        model = Account
        fields = ("first_name", "last_name", "username", "email", "account_type", "password1", "password2")
