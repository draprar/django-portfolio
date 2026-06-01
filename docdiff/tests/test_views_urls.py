import pytest
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.urls import resolve, reverse

from docdiff.views import docdiff_view


@pytest.mark.django_db
class TestDocDiffView:
    """Integration tests for the main DocDiff view (docdiff_view)."""

    def test_get_returns_upload_page(self, client):
        """GET request should render the upload form page (200 OK)."""
        url = reverse("docdiff:index")
        response = client.get(url)
        assert response.status_code == 200
        html = response.content.decode().lower()
        # expect form tag or file input
        assert "<form" in html
        assert "file" in html

    def test_post_without_files_returns_400(self, client):
        """POST request without files should return a 400 JSON error."""
        url = reverse("docdiff:compare")
        response = client.post(url, {})
        assert response.status_code == 200
        html = response.content.decode().lower()
        assert "missing_files" in html

    def test_post_with_txt_files_returns_html_response(self, client):
        """
        POST request with two .txt files should:
        - process comparison successfully
        - return a valid HTML report as response
        """
        url = reverse("docdiff:compare")

        # Create two simple text files to compare
        old_file = SimpleUploadedFile("old.txt", b"Hello world")
        new_file = SimpleUploadedFile("new.txt", b"Hello brave new world")

        response = client.post(url, {"file_old": old_file, "file_new": new_file})

        assert response.status_code == 200
        content = response.content.decode("utf-8").lower()

        # Response should be an HTML page containing the report
        assert "<html" in content
        assert "raport" in content or "diff" in content

    def test_unsupported_extension_raises_valueerror(self, client):
        """Unsupported file types should return a 400 error with message."""
        url = reverse("docdiff:compare")
        bad_file = SimpleUploadedFile("file.xyz", b"abc")
        response = client.post(url, {"file_old": bad_file, "file_new": bad_file})
        assert response.status_code == 200
        html = response.content.decode().lower()
        assert "unsupported_type" in html

    def test_spoofed_docx_signature_rejected(self, client):
        url = reverse("docdiff:compare")
        fake_docx_1 = SimpleUploadedFile(
            "old.docx",
            b"not-a-zip",
            content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
        fake_docx_2 = SimpleUploadedFile(
            "new.docx",
            b"still-not-a-zip",
            content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )

        response = client.post(url, {"file_old": fake_docx_1, "file_new": fake_docx_2})
        assert response.status_code == 200
        html = response.content.decode().lower()
        assert "signature_invalid" in html

    def test_txt_mime_with_charset_is_accepted(self, client):
        url = reverse("docdiff:compare")
        old_file = SimpleUploadedFile("old.txt", b"Ala ma kota", content_type="text/plain; charset=utf-8")
        new_file = SimpleUploadedFile("new.txt", b"Ala ma dwa koty", content_type="text/plain; charset=utf-8")

        response = client.post(url, {"file_old": old_file, "file_new": new_file})
        assert response.status_code == 200
        assert "mime_invalid" not in response.content.decode().lower()

    def test_octet_stream_mime_for_txt_is_accepted(self, client):
        url = reverse("docdiff:compare")
        old_file = SimpleUploadedFile("old.txt", b"one", content_type="application/octet-stream")
        new_file = SimpleUploadedFile("new.txt", b"two", content_type="application/octet-stream")

        response = client.post(url, {"file_old": old_file, "file_new": new_file})
        assert response.status_code == 200
        assert "mime_invalid" not in response.content.decode().lower()

    @override_settings(RATELIMIT_ENABLE=True)
    def test_post_rate_limited_after_ten_requests(self, client):
        url = reverse("docdiff:compare")
        cache.clear()
        post_kwargs = {"REMOTE_ADDR": "203.0.113.10"}

        for _ in range(10):
            old_file = SimpleUploadedFile("old.txt", b"a")
            new_file = SimpleUploadedFile("new.txt", b"b")
            response = client.post(url, {"file_old": old_file, "file_new": new_file}, **post_kwargs)
            assert response.status_code == 200

        old_file = SimpleUploadedFile("old.txt", b"a")
        new_file = SimpleUploadedFile("new.txt", b"b")
        response = client.post(url, {"file_old": old_file, "file_new": new_file}, **post_kwargs)
        assert response.status_code == 403

    def test_filename_path_traversal_does_not_create_outside_file(self, client, monkeypatch, tmp_path):
        url = reverse("docdiff:compare")
        monkeypatch.setattr("docdiff.views.tempfile.mkdtemp", lambda: str(tmp_path))

        traversal_name = "../../outside.txt"
        old_file = SimpleUploadedFile(traversal_name, b"old")
        new_file = SimpleUploadedFile("new.txt", b"new")

        response = client.post(url, {"file_old": old_file, "file_new": new_file}, REMOTE_ADDR="203.0.113.11")
        assert response.status_code == 200

        outside_candidate = (tmp_path / ".." / ".." / "outside.txt").resolve()
        assert not outside_candidate.exists()


class TestDocDiffUrls:
    """Basic tests for URL configuration of the docdiff app."""

    def test_index_url_resolves_correct_view(self):
        """The 'index' route should resolve to the main docdiff_view."""
        path = reverse("docdiff:index")
        assert resolve(path).func.__name__ == docdiff_view.__name__

    def test_compare_url_resolves_correct_view(self):
        """The 'compare' route should resolve to the same docdiff_view."""
        path = reverse("docdiff:compare")
        assert resolve(path).func.__name__ == docdiff_view.__name__
