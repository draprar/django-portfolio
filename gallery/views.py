from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import generic
from rest_framework import filters, generics

from .forms import CategoryForm, GalleryForm
from .models import Category, Gallery, InstagramPost
from .serializers import CategorySerializer, GallerySerializer


def _home_url(view: str, category: str) -> str:
    params: dict[str, str] = {}
    if category and category != "All":
        params["category"] = category
    if view == "grid":
        params["view"] = "grid"
    base = reverse("gallery:gallery_home")
    if not params:
        return base
    return f"{base}?{urlencode(params)}"


def _slot(index: int, total: int) -> str:
    if index == 0:
        return "active"
    if total > 2 and index == total - 1:
        return "prev"
    if index == 1:
        return "next"
    return "off"


def _category_items(category, instagram_posts) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    if category.title == "Instagram":
        for post in instagram_posts:
            caption = post.location or post.caption or "bazgrollin'"
            for media in post.media.all():
                if media.is_video and media.video:
                    src = media.video.url
                    kind = "video"
                elif media.image:
                    src = media.image.url
                    kind = "image"
                else:
                    continue
                items.append(
                    {
                        "kind": kind,
                        "src": src,
                        "title": caption,
                        "kicker": category.title,
                        "caption": caption,
                    }
                )
    else:
        for art in category.images.all():
            title = (art.title or "").strip() or category.title
            caption = art.title or art.description or category.title
            items.append(
                {
                    "kind": "image",
                    "src": art.image.url,
                    "title": title,
                    "kicker": category.title,
                    "caption": caption,
                }
            )
    total = len(items)
    for index, item in enumerate(items):
        item["slot"] = _slot(index, total)
    return items


def _carousel_groups(categories, instagram_posts, selected: str) -> list[dict]:
    """One hub-style carousel per category, in category order."""
    groups = []
    for category in categories:
        if selected != "All" and selected != category.title:
            continue
        groups.append(
            {
                "id": category.id,
                "title": category.title,
                "items": _category_items(category, instagram_posts),
            }
        )
    return groups


class Home(generic.TemplateView):
    """
    Gallery homepage. Category filtering happens in the template from
    `selected_category`; images are loaded via Category.images prefetch.
    Default presentation is one 3D carousel per category; `?view=grid` keeps the grid.
    """

    template_name = "gallery/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.request.GET.get("category") or None
        selected = category if category else "All"
        view_mode = "grid" if self.request.GET.get("view") == "grid" else "carousel"
        categories = Category.objects.all().prefetch_related("images").order_by("order", "title")
        instagram_posts = InstagramPost.objects.all().prefetch_related("media").order_by("-created_at")
        context["selected_category"] = selected
        context["view_mode"] = view_mode
        context["categories"] = categories
        context["instagram_posts"] = instagram_posts
        context["carousel_groups"] = _carousel_groups(categories, instagram_posts, selected)
        context["carousel_url"] = _home_url("carousel", selected)
        context["grid_url"] = _home_url("grid", selected)
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
