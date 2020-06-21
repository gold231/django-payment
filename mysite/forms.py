from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class UserSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, help_text='Required', widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=100, help_text='Required', widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    username = forms.CharField(max_length=100, help_text='Required', widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email = forms.EmailField(max_length=100, help_text='Required', widget=forms.EmailInput(attrs={'placeholder': 'Email Address'}))
    password1 = forms.CharField(max_length=100, help_text='Required', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(max_length=100, help_text='Required', widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

class UserSignInForm(AuthenticationForm):
    username = forms.CharField(max_length=100, help_text='Required', widget=forms.TextInput(attrs={'placeholder': ' Username'}))
    password = forms.CharField(max_length=100, help_text='Required', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    class Meta:
        model = User
        fields = ('username', 'password')