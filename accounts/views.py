from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.context_processors import csrf

from accounts.forms import UserRegistrationForm, UserAuthenticationForm
from courses.models import Course, Slide


# @login_required(login_url="login/")
def profile(request):
    courses = []
    for course in Course.objects.filter(author=User.objects.get(username=request.user.username)):
        cover = Slide.objects.get(course=course, number=0)
        courses.append({"id": course.id,
                        "title": course.title,
                        "description": course.description,
                        "cover": cover.image})

    return render(request, "accounts/profile.html", {"courses": courses})


def login_user(request):
    form = UserAuthenticationForm(request.POST or None)
    print(form.errors)
    print("here")
    if request.method == 'POST':
        print("here")
        if form.is_valid():
            user = form.login(request)
            print("here")
            if user:
                login(request, user)
                print("here")
                return HttpResponseRedirect("/accounts/profile")

    data = {}
    data.update(csrf(request))
    data["form"] = form
    return render(request, "accounts/login.html", data)


def register_user(request):
    form = UserRegistrationForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            user = authenticate(username=form.cleaned_data["username"],
                                password=form.cleaned_data["password1"])
            login(request, user)
            return HttpResponseRedirect("/accounts/profile")

    data = {}
    data.update(csrf(request))
    data["form"] = form
    return render(request, "accounts/register.html", data)
