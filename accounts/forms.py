from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from django.utils.translation import ugettext_lazy as _


class UserAuthenticationForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Имя пользователя"}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Пароль"})
    )

    class Meta:
        model = User
        fields = ("username", "password")

    def clean(self):
        user = authenticate(username=self.cleaned_data['username'],
                            password=self.cleaned_data['password'])
        if not user:
            raise forms.ValidationError("Неверное имя пользователя или пароль.")
        if not user.is_active:
            raise forms.ValidationError("Пользователь уже авторизован.")

        return self.cleaned_data

    def login(self, request):
        user = authenticate(username=self.cleaned_data['username'],
                            password=self.cleaned_data['password'])
        return user


class UserRegistrationForm(forms.ModelForm):
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
            raise forms.ValidationError("Пользователь с таким именем уже существует")
        except User.DoesNotExist:
            return username

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")
        if len(password1) < 8:
            raise forms.ValidationError("Пароль слишком короткий, он должен содержать минимум 8 символов")

        return password2

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.username = self.cleaned_data["username"]
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
