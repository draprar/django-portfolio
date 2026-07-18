from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models


class Category(models.Model):
    """
    Represents a category to organize gallery images.
    """

    title = models.CharField(max_length=150, unique=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Gallery(models.Model):
    """
    Represents an image in the gallery with an optional description.
    Each image belongs to a specific category.
    """

    category = models.ForeignKey(Category, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images")
    title = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.image.url


class Contact(models.Model):
    """
    Represents a contact form submission.
    """

    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"


class InstagramPost(models.Model):
    """
    Represents a manually added, Instagram-style post. A post can contain
    one or several photos (like an Instagram carousel) and is displayed
    with a location header and a caption, in the style of an IG post.
    """

    category = models.ForeignKey("Category", related_name="instagram_posts", on_delete=models.CASCADE)
    location = models.CharField(max_length=255, blank=True, null=True)
    caption = models.TextField(blank=True, null=True)
    permalink = models.URLField(
        blank=True,
        null=True,
        help_text="Optional link to the original Instagram post (shown as a small IG icon).",
    )
    created_at = models.DateTimeField()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Post in {self.category.title} - {self.created_at}"


class InstagramPostMedia(models.Model):
    """
    A single piece of media belonging to an InstagramPost: either a photo
    or a reel (video). A post can have several of these (carousel-style),
    ordered by the `order` field.
    """

    post = models.ForeignKey(InstagramPost, related_name="media", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="instagram", blank=True, null=True)
    video = models.FileField(
        upload_to="instagram/reels",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=["mp4", "mov", "webm"])],
        help_text="Upload a reel here instead of an image. Leave the image field empty.",
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def clean(self):
        if not self.image and not self.video:
            raise ValidationError("Dodaj zdjęcie albo wideo (rolkę).")
        if self.image and self.video:
            raise ValidationError("Wybierz tylko jedno: zdjęcie albo wideo, nie oba naraz.")

    @property
    def is_video(self):
        return bool(self.video)

    def __str__(self):
        kind = "Video" if self.is_video else "Image"
        return f"{kind} #{self.order} for post {self.post_id}"