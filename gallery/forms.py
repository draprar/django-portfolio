from django import forms

from .models import Category, Gallery


class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ["category", "image", "title", "description"]


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["title"]
