from django import forms
from django.forms import EmailField, CharField, ModelForm
from .models import UserProfile
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class UserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.firstname = self.cleaned_data["first_name"]
        user.lastname = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user

class EditProfileForm(UserChangeForm):
    password = None

    class Meta():
        model = User
        fields = ("username", "email", "first_name", "last_name")


class EditAvatar(ModelForm):
    
    class Meta:
        model = UserProfile
        fields = ('image',)