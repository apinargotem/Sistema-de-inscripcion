from django import forms

from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.models import User
from usuario.models import User

class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "cedula", "email", "password1", "password2"]

    def clean_username(self):
        username = self.cleaned_data['username']
        return username.lower() if username else username



    def save(self, commit=True):
        # self.username= self.username.lower() if self.username else ''
        return super(CustomUserCreationForm, self).save(commit)

