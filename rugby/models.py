from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE)

    title_pl = models.CharField(max_length=255, verbose_name="Tytuł (PL)")
    title_en = models.CharField(max_length=255, verbose_name="Title (EN)", blank=True)

    text_pl = models.TextField(verbose_name="Treść (PL)")
    text_en = models.TextField(verbose_name="Text (EN)", blank=True)

    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title_pl

    class Meta:
        ordering = ["published_date"]
