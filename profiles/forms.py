from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Profile


class UserCreateForm(UserCreationForm):
    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")
    email = forms.EmailField(label="Email")

    class Meta:
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2"
        )
        model = User

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"].title()
        user.last_name = self.cleaned_data["last_name"].title()
        user.email = self.cleaned_data["email"].lower()
        if commit:
            user.save()
        return user


class UserUpdateAccount(UserChangeForm):

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "password",
        )

    def save(self, commit=True):
        user = super(UserUpdateAccount, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"].title()
        user.last_name = self.cleaned_data["last_name"].title()
        user.email = self.cleaned_data["email"].lower()
        if commit:
            user.save()
        return user


class UserUpdateProfile(forms.ModelForm):

    class Meta:
        model = Profile
        fields = (
            "location",
            "bio",
            "profile_pic",
        )
