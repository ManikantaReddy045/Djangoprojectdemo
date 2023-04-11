from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model, login
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from djangodemoprojectcokkiecuter.users.models import *

User = get_user_model()


class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User

        error_messages = {
            "username": {"unique": _("This username has already been taken.")}
        }

    def username(self):
        username = self.cleaned_data["username"]

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username

        raise ValidationError(self.error_messages["duplicate_username"])


class UserSignupForm(SignupForm):
    """
    Form that will be rendered on a user sign up section/screen.
    Default fields will be added automatically.
    Check UserSocialSignupForm for accounts created from social.
    """


class MyCustomSignupForm(forms.Form):
    """
    Form that will be rendered on a user sign up section/screen.
    Default fields will be added automatically.
    Check UserSocialSignupForm for accounts created from social.
    """

    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=12)
    password1 = forms.CharField(max_length=100)
    password2 = forms.CharField(max_length=100)

    def clean_password1(self):
        value = self.cleaned_data["password1"]
        if len(value) < 8:
            raise ValidationError("Password length must be 8 chars")
        return value

    def clean(self):
        attr = super().clean()
        if attr.get("password1") != attr.get("password2"):
            raise ValidationError("Passwords did not match")
        return attr

    def clean_phone_number(self):
        phone_no = self.cleaned_data["phone_number"]
        try:
            int(phone_no)
        except (ValueError, TypeError):
            raise ValidationError("Please enter a valid phone number")
        return phone_no

    def save(self):
        validated_data = self.clean()
        user = User(
            username=validated_data.get("username"),
            phone_numbers=validated_data.get("phone_number"),
            email=validated_data.get("email"),
        )
        user.set_password(validated_data.get("password1"))
        user.save()
        return user


class MyCustomLoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)


class MyCustomOtpLoginForm(forms.Form):
    phone_number = forms.CharField(max_length=100)


class UserSocialSignupForm(SocialSignupForm):
    """
    Renders the form when user has signed up using social accounts.
    Default fields will be added automatically.
    See UserSignupForm otherwise.
    """
