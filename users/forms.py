# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='A valid email address is required.')
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email','first_name','last_name','organization','user_type',)

class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ('username', 'email','first_name','last_name','organization','user_type',)

