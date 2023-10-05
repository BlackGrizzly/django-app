from django import forms
from django.core import validators
from django.contrib.auth.models import User
from .models import Profile

class DateInput(forms.DateInput):
    input_type = 'date'

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "avatar", "bio", "birthday", "agreement_accepted"
        widgets = {
            'birthday': DateInput(),
        }