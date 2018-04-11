from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.context_processors import csrf

from accounts.forms import UserRegistrationForm
from courses.models import Course, Slide


@login_required(login_url="login/")
def profile(request):

    courses = []
    for course in Course.objects.filter(author=User.objects.get(username=request.user.username)):
        cover = Slide.objects.get(course=course, number=0)
        courses.append({"id": course.id,
                        "title": course.title,
                        "description": course.description,
                        "cover": cover.image})

    return render(request, "accounts/profile.html", {"courses": courses})


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
