from django import forms
from django.contrib.auth.models import User

class SignUpForm(forms.Form):
    first_name = forms.CharField(max_length=65, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=65, widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(max_length=65, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    conf_password = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class LoginForm(forms.Form):
    username = forms.CharField(max_length=65, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class QuantityForm(forms.Form):
    quantity = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))
