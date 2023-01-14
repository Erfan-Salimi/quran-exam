from django import forms
from .models import *


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=10)

class QuestionForm(forms.Form):
    answer = forms.CharField(max_length=10)