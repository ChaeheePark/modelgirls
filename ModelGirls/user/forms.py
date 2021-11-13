from django import forms
from django.contrib.auth.models import User

from .models import Profile

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name','last_name']

class ProfileForm(forms.ModelForm):
    image = forms.ImageField(required=False) # 선택적으로 입력할 수 있음.
    class Meta:
        model = Profile
        fields = ['nickname','image', 'bio']

