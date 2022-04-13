from attr import attr
from django.contrib.auth import forms as auth_forms
from django import forms
from matplotlib import widgets

class RegisterNewCustomer(auth_forms.UserCreationForm):
    pass

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=100,)
    password = forms.CharField(widget=forms.PasswordInput,)
    email = forms.CharField(widget=forms.EmailInput)
    
   