from django.contrib.auth.views import login, logout
from django.urls import path

from accounts.forms import UserAuthenticationForm
from . import views

urlpatterns = [
    path(r"", login, {"template_name": "accounts/login.html",
                      "authentication_form": UserAuthenticationForm}, name="login"),
    path(r"logout/", logout, {"next_page": "/"}, name="logout"),
    path(r"register/", views.register, name="register"),
    path(r"profile/", views.profile, name="profile")
]
