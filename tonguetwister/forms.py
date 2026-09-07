from django import forms
from django.contrib.auth.forms import SetPasswordForm, UserCreationForm
from django.contrib.auth.models import Group, User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import transaction
from PIL import Image, UnidentifiedImageError

from .models import Articulator, Exercise, Funfact, OldPolish, Profile, Trivia, Twister
from .services import REGISTER_FAILURE_MESSAGE


# Form to create or edit Articulator model instances
class ArticulatorForm(forms.ModelForm):
    class Meta:
        model = Articulator
        fields = ["text"]  # Field included in the form


# Form to create or edit Exercise model instances
class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ["text"]  # Field included in the form


# Form to create or edit Twister model instances
class TwisterForm(forms.ModelForm):
    class Meta:
        model = Twister
        fields = ["text"]  # Field included in the form


# Form to create or edit Trivia model instances
class TriviaForm(forms.ModelForm):
    class Meta:
        model = Trivia
        fields = ["text"]  # Field included in the form


# Form to create or edit Funfact model instances
class FunfactForm(forms.ModelForm):
    class Meta:
        model = Funfact
        fields = ["text"]  # Field included in the form


# Form to create or edit OldPolish model instances
class OldPolishForm(forms.ModelForm):
    class Meta:
        model = OldPolish
        fields = ["old_text", "new_text"]  # Fields included in the form


# Password validator for strong passwords
strong_password_validator = RegexValidator(
    regex=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+]).{8,}$",
    message="Hasło powinno mieć więcej niż 8 znaków i zawierać: wielkie i małe litery, cyfry i znaki specjalne.",
)


class StrongSetPasswordForm(SetPasswordForm):
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("new_password1")
        if password:
            strong_password_validator(password)
        return cleaned_data


# Custom user creation form for registration, inheriting from UserCreationForm
class CustomUserCreationForm(UserCreationForm):
    # Custom fields with additional validators and widgets
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"id": "username"}),
        error_messages={"unique": REGISTER_FAILURE_MESSAGE},
    )
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"id": "email"}))
    password1 = forms.CharField(
        required=True,
        validators=[strong_password_validator],  # Enforces strong password policy
        widget=forms.PasswordInput(attrs={"id": "password1"}),
    )
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={"id": "password2"}))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")  # Fields to include in the form
        error_messages = {
            "username": {"unique": REGISTER_FAILURE_MESSAGE},
        }

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise ValidationError(REGISTER_FAILURE_MESSAGE)
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError(REGISTER_FAILURE_MESSAGE)
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Hasełka do siebie nie pasują :(")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            with transaction.atomic():
                user.save()
                regular_users_group, _created = Group.objects.get_or_create(name="Regular Users")
                user.groups.add(regular_users_group)
        return user


# Form for uploading a profile avatar with custom validation
class AvatarUploadForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["avatar"]  # Only avatar field included in the form
        widgets = {
            "avatar": forms.FileInput(
                attrs={
                    "class": "form-control-file",
                    "id": "avatar",
                }
            ),
        }
        labels = {
            "avatar": "Wybierz awatar"  # Custom label for the avatar field
        }

    # Custom validation for avatar field
    def clean_avatar(self):
        avatar = self.cleaned_data.get("avatar")

        if not avatar:
            raise ValidationError("Wybierz awatar.")  # Error if no avatar is selected

        valid_mime_types = ["image/jpeg", "image/jpg", "image/png", "image/gif"]
        if avatar.content_type not in valid_mime_types:
            raise ValidationError(
                "Niepoprawny format pliku. Akceptowane formaty to JPEG/JPG, PNG, GIF."
            )  # Error for invalid file type

        max_file_size = 2 * 1024 * 1024  # 2 MB file size limit
        if avatar.size > max_file_size:
            raise ValidationError("Rozmiar pliku nie może przekroczyć 2 MB.")  # Error if file exceeds size limit

        try:
            avatar.seek(0)
            with Image.open(avatar) as image:
                image.verify()
        except (UnidentifiedImageError, OSError, ValueError, SyntaxError):
            raise ValidationError("Niepoprawny format pliku. Akceptowane formaty to JPEG/JPG, PNG, GIF.")
        avatar.seek(0)

        return avatar
