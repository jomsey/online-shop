from django.contrib.auth import forms as auth_forms
from django import forms
from .models import ProductInstance


class RegisterNewCustomer(auth_forms.UserCreationForm):
    pass

class ProductInstanceForm(forms.ModelForm):
    class Meta:
        model = ProductInstance
        fields = ('product_count',)



