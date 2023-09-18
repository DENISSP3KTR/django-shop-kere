from typing import Any, Dict
from django import forms
import store
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput())


class RegisterForm(forms.Form):
    last_name = forms.CharField(required=True)
    first_name = forms.CharField(required=True)
    patronymic = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput())
    confirmpassword = forms.CharField(widget=forms.PasswordInput())
    sogl = forms.BooleanField(required=True)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirmpassword = cleaned_data.get('confirmpassword')

        if password and confirmpassword and password != confirmpassword:
            raise forms.ValidationError("Пароли не совпадают.")

        return cleaned_data
    
class ProductSearchForm(forms.Form):
    query = forms.CharField(max_length=100)