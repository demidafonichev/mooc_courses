from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from django.utils.translation import ugettext_lazy as _


class UserAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Имя пользователя или почта"}),
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
        widget=forms.TextInput(attrs={"placeholder": "Имя пользователя или почта"}),
    )
    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Фамилия"})
    )
    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Имя"})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Пароль"})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Повторите пароль"})
    )

    class Meta:
        model = User
        fields = ("username", "last_name", "first_name", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data["username"]
        try:
            User.objects.get(email=email)
            raise forms.ValidationError("Email already registered")
        except User.DoesNotExist:
            return email

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.username = self.cleaned_data["username"]
        user.email = self.cleaned_data["username"]
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
