import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils.timezone import now

from gallery.models import Category, Gallery, InstagramPost, InstagramPostMedia


@pytest.mark.django_db
def test_category_creation():
    # Create a category
    category = Category.objects.create(title="Drawings")

    # Assert category fields
    assert category.title == "Drawings"
    assert str(category) == "Drawings"


@pytest.mark.django_db
def test_category_unique_constraint():
    # Create a category
    Category.objects.create(title="Drawings")

    # Attempt to create a category with the same title
    with pytest.raises(ValidationError):
        category = Category(title="Drawings")
        category.full_clean()  # Validate the model instance


@pytest.mark.django_db
def test_gallery_creation():
    # Create a category
    category = Category.objects.create(title="Drawings")

    # Create a gallery item
    gallery = Gallery.objects.create(
        category=category,
        image="test_image.jpg",
        description="A beautiful drawing.",
    )

    # Assert gallery fields
    assert gallery.description == "A beautiful drawing."
    assert gallery.category == category
    assert gallery.image.name == "test_image.jpg"
    assert str(gallery) == gallery.image.url


@pytest.mark.django_db
def test_gallery_ordering():
    # Create a category
    category = Category.objects.create(title="Drawings")

    # Create multiple gallery items
    gallery1 = Gallery.objects.create(category=category, image="image1.jpg", created_at=now())
    gallery2 = Gallery.objects.create(category=category, image="image2.jpg", created_at=now())

    # Assert ordering by ID
    galleries = list(Gallery.objects.all())
    assert galleries[0] == gallery1
    assert galleries[1] == gallery2


@pytest.mark.django_db
def test_gallery_deletion_with_category():
    # Create a category
    category = Category.objects.create(title="Drawings")

    # Create a gallery item linked to the category
    Gallery.objects.create(
        category=category,
        image="test_image.jpg",
        description="A beautiful drawing.",
    )

    # Delete the category
    category.delete()

    # Assert the gallery item is deleted
    assert Gallery.objects.count() == 0


@pytest.mark.django_db
def test_instagram_post_creation():
    category = Category.objects.create(title="Photography")
    post = InstagramPost.objects.create(
        caption="Sample caption",
        location="Kraków",
        created_at=now(),
        category=category,
    )
    assert post.caption == "Sample caption"
    assert post.location == "Kraków"
    assert post.category == category
    assert str(post) == f"Post in {category.title} - {post.created_at}"


@pytest.mark.django_db
def test_instagram_media_accepts_image_xor_video():
    category = Category.objects.create(title="Photography")
    post = InstagramPost.objects.create(caption="cap", created_at=now(), category=category)
    media = InstagramPostMedia.objects.create(post=post, image="instagram/photo.jpg")
    media.full_clean()
    assert media.is_video is False

    video_media = InstagramPostMedia.objects.create(post=post, video="instagram/reels/clip.mp4", order=1)
    video_media.full_clean()
    assert video_media.is_video is True


@pytest.mark.django_db
def test_instagram_media_rejects_both_or_neither():
    category = Category.objects.create(title="Photography")
    post = InstagramPost.objects.create(caption="cap", created_at=now(), category=category)

    both = InstagramPostMedia(post=post, image="instagram/photo.jpg", video="instagram/reels/clip.mp4")
    with pytest.raises(ValidationError):
        both.full_clean()

    neither = InstagramPostMedia(post=post)
    with pytest.raises(ValidationError):
        neither.full_clean()

    with pytest.raises(IntegrityError):
        InstagramPostMedia.objects.create(post=post, image="instagram/photo.jpg", video="instagram/reels/clip.mp4")
