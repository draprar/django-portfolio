from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import generic
from rest_framework import filters, generics

from .forms import CategoryForm, GalleryForm
from .models import Category, Gallery, InstagramPost
from .serializers import CategorySerializer, GallerySerializer


class Home(generic.TemplateView):
    """
    Gallery homepage. Category filtering happens in the template from
    `selected_category`; images are loaded via Category.images prefetch.
    """

    template_name = "gallery/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.request.GET.get("category") or None
        context["selected_category"] = category if category else "All"
        context["categories"] = Category.objects.all().prefetch_related("images").order_by("order", "title")
        context["instagram_posts"] = InstagramPost.objects.all().prefetch_related("media").order_by("-created_at")
        return context


class AdminOnlyMixin(UserPassesTestMixin):
    """
    Mixin to restrict access to admin-only views.
    """

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        """
        Redirects unauthorized users to the home page with an error message.
        """
        messages.error(self.request, "You do not have permission to perform this action.")
        return redirect("gallery:gallery_home")


class UploadImage(AdminOnlyMixin, generic.CreateView):
    """
    View for admins to upload a new image to the gallery.
    """

    model = Gallery
    template_name = "gallery/upload-image.html"
    form_class = GalleryForm
    success_url = reverse_lazy("gallery:gallery_home")

    def form_valid(self, form):
        """
        Handle successful form submission with a success message.
        """
        messages.success(self.request, "Image uploaded successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Handle form errors with a user-friendly message.
        """
        messages.error(self.request, "Failed to upload image. Please correct the errors.")
        return super().form_invalid(form)


class DeleteImage(AdminOnlyMixin, generic.DeleteView):
    """
    View for admins to delete an existing image from the gallery.
    """

    model = Gallery
    template_name = "gallery/delete-image.html"
    success_url = reverse_lazy("gallery:gallery_home")

    def get_object(self, queryset=None):
        """
        Retrieves the image object based on the primary key.
        """
        return get_object_or_404(Gallery, pk=self.kwargs["pk"])


class CreateCategory(AdminOnlyMixin, generic.CreateView):
    """
    View for admins to create a new image category.
    """

    model = Category
    template_name = "gallery/create-category.html"
    form_class = CategoryForm
    success_url = reverse_lazy("gallery:upload-image")


def custom_404(request, exception):
    """
    Custom 404 error view.
    Renders the 404.html template with a 404 status code.
    """
    return render(request, "gallery/404.html", status=404)


def custom_500(request):
    """
    Custom 500 error view.
    Renders the 500.html template with a 500 status code.
    """
    return render(request, "gallery/500.html", status=500)


class CategoryListView(generics.ListAPIView):
    """
    API view to retrieve a list of all categories.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GalleryListView(generics.ListAPIView):
    """
    API view to retrieve a list of all gallery items, with optional filtering by category.
    """

    queryset = Gallery.objects.select_related("category").all()
    serializer_class = GallerySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["category__title", "title"]  # Enable searching by category or image title
