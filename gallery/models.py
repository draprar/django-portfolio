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


class InstagramPostImage(models.Model):
    """
    A single photo belonging to an InstagramPost. Supports multiple photos
    per post (carousel-style), ordered by the `order` field.
    """

    post = models.ForeignKey(InstagramPost, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="instagram")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"Image #{self.order} for post {self.post_id}"