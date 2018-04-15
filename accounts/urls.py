from django.contrib.auth.views import logout
from django.urls import path

from . import views

urlpatterns = [
    path(r"login_user/", views.login_user, name="login_user"),
    path(r"register_user/", views.register_user, name="register_user"),
    path(r"logout/", logout, {"next_page": "/"}, name="logout"),
    path(r"profile/", views.profile, name="profile")
]
