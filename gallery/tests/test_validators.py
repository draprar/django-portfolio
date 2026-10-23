from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile

from gallery.models import validate_gallery_image_size


def test_gallery_image_size_rejects_oversized():
    big = SimpleUploadedFile("big.jpg", b"x" * (5 * 1024 * 1024 + 1), content_type="image/jpeg")
    try:
        validate_gallery_image_size(big)
        raised = False
    except ValidationError:
        raised = True
    assert raised


def test_gallery_image_size_allows_small():
    small = SimpleUploadedFile("ok.jpg", b"tiny", content_type="image/jpeg")
    validate_gallery_image_size(small)
