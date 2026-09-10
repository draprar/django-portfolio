from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

CONTACT_MESSAGE_MAX_LENGTH = 5000


def validate_file_size(file):
    max_mb = 5
    if file.size > max_mb * 1024 * 1024:
        raise ValidationError(_(f"Max file size is {max_mb} MB"))


class Project(models.Model):
    title_en = models.CharField(max_length=200)
    title_pl = models.CharField(max_length=200)
    desc_en = models.TextField(blank=True, help_text="Full CV description for / (recruiter landing).")
    desc_pl = models.TextField(blank=True, help_text="Full CV description for / (recruiter landing).")
    desc_code_en = models.TextField(
        blank=True,
        help_text="Short kodzillin'-style blurb for /code/ (EN). Falls back to desc_en if empty.",
    )
    desc_code_pl = models.TextField(
        blank=True,
        help_text="Short kodzillin'-style blurb for /code/ (PL). Falls back to desc_pl if empty.",
    )
    github_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    image = models.ImageField(
        upload_to="projects/",
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "gif", "webp"]),
            validate_file_size,
        ],
        help_text="Allowed: jpg, png, gif, webp. Max 5 MB.",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title_en} / {self.title_pl}"

    @property
    def display_desc_en(self) -> str:
        """Return short code desc if available, else CV desc."""
        return self.desc_code_en or self.desc_en

    @property
    def display_desc_pl(self) -> str:
        """Return short code desc if available, else CV desc."""
        return self.desc_code_pl or self.desc_pl


class Contact(models.Model):
    """
    Represents a contact form submission from the portfolio page.
    """

    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField(max_length=CONTACT_MESSAGE_MAX_LENGTH)
    submitted_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-submitted_at"]
        verbose_name = "Contact Submission"
        verbose_name_plural = "Contact Submissions"

    def __str__(self):
        return f"Message from {self.name} ({self.submitted_at.strftime('%Y-%m-%d %H:%M')})"
