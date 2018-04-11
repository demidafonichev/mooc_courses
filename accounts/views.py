from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.context_processors import csrf

from accounts.forms import UserRegistrationForm


@login_required(login_url="login/")
def profile(request):
    return render(request, "accounts/profile.html")


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=form.cleaned_data["username"],
                                password=form.cleaned_data["password1"])
            login(request, user)
            return HttpResponseRedirect("/accounts/profile")

    token = {}
    token.update(csrf(request))
    token["form"] = UserRegistrationForm()
    token["is_user_authenticated"] = request.user.is_authenticated

    return render(request, "accounts/register.html", token)
