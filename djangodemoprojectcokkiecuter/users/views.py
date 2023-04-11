import os
import random

from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView

from djangodemoprojectcokkiecuter.users.forms import *
from djangodemoprojectcokkiecuter.users.verify import *

from .verify import *

# from allauth.account.app_settings import EmailVerificationMethod
User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        assert (
            self.request.user.is_authenticated
        )  # for mypy to know that the user is authenticated
        return self.request.user.get_absolute_url()

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


def EmailVerificationRedirectView(request):
    response = HttpResponse("", status=302)
    if os.environ["DJANGO_SETTINGS_MODULE"] == "config.settings.local":
        response["Location"] = "http://127.0.0.1:8025/#"
    else:
        response["Location"] = ""

    return response


def otplogin(request):
    if request.method == "POST":
        phone_numbers = request.POST.get("phone_numbers")
        profile = User.objects.get(phone_numbers=phone_numbers)
        profiles = random.randint(1000, 9999)
        profile.phone_otp = profiles
        profile.save()
        print()
        message_handler = SendOTP(phone_numbers, profile.phone_otp).send_code()
        return render(request, "account/otp.html")

    return render(request, "account/otplogin.html")


def otp(request):
    print("-----------otp is called")
    if request.method == "POST":
        otp = request.POST.get("phone_otp")
        user = User.objects.get(phone_otp=otp)
        if otp == user.phone_otp:
            return render(request, "pages/about.html")
        else:
            return render(request, "account/otp.html")


def register(request):
    if request.method == "POST":
        form = MyCustomSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to="login_view")
    else:
        form = MyCustomSignupForm()
    return render(request, "account/register.html", {"form": form})


def loginnew(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        form = MyCustomLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=username, password=password)
            print(user)
            if user:
                login(request, user)
            else:
                raise forms.ValidationError(
                    "The username you have entered does not exist."
                )
            return redirect(to="about")
    else:
        form = MyCustomLoginForm()
    return render(request, "account/new_login.html", {"form": form})
