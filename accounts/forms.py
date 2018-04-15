from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from django.utils.translation import ugettext_lazy as _


class UserAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Имя пользователя"}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Пароль"})
    )

    class Meta:
        fields = ("username", "password")


class UserRegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)

    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Имя пользователя"}),
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Пароль"})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Повторите пароль"})
    )

    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
            raise forms.ValidationError("Username already registered.")
        except User.DoesNotExist:
            return username

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.username = self.cleaned_data["username"]
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
