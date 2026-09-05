from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models


def validate_avatar_size(file):
    max_mb = 2
    if file.size > max_mb * 1024 * 1024:
        raise ValidationError(f"Rozmiar pliku nie może przekroczyć {max_mb} MB.")


# Represents a tongue twister
class Twister(models.Model):
    text = models.TextField()  # Stores the text of the twister

    def __str__(self):
        # Returns the text when the object is represented as a string
        return self.text


# Represents an articulator
class Articulator(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text


# Represents an exercise
class Exercise(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text


# Represents trivia
class Trivia(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text


# Represents fun fact
class Funfact(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text


# Represents Old Polish phrases along with modern equivalents
class OldPolish(models.Model):
    old_text = models.TextField()  # Stores the Old Polish version of the phrase
    new_text = models.TextField()  # Stores the modern translation of the phrase

    def __str__(self):
        # Returns a formatted string that shows both Old Polish and modern translation
        return f"Czy wiesz, że staropolskie {self.old_text} można przetłumaczyć jako {self.new_text}?"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # One-to-one relationship with User model
    avatar = models.ImageField(
        upload_to="avatars/%Y/%m/%d/",
        null=True,
        blank=True,
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "gif"]),
            validate_avatar_size,
        ],
        help_text="Allowed: jpg, jpeg, png, gif. Max 2 MB.",
    )
    email_confirmed = models.BooleanField(default=False)  # Indicates if the user has confirmed their email

    def __str__(self):
        return f"{self.user.username} Profile"


# Represents the many-to-many relationship between a user and user articulators
class UserProfileArticulator(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Links to the User model
    articulator = models.ForeignKey(Articulator, on_delete=models.CASCADE)  # Links to an Articulator object

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "articulator"], name="uniq_user_articulator"),
        ]


# Represents the many-to-many relationship between a user and user exercises
class UserProfileExercise(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Links to the User model
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)  # Links to an Exercise object

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "exercise"], name="uniq_user_exercise"),
        ]


# Represents the many-to-many relationship between a user and user twisters
class UserProfileTwister(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Links to the User model
    twister = models.ForeignKey(Twister, on_delete=models.CASCADE)  # Links to a Twister object

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "twister"], name="uniq_user_twister"),
        ]
