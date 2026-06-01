import pytest
from django.contrib.auth.models import User
from django.utils import timezone

from rugby.models import Post


@pytest.mark.django_db
class TestPostModel:
    def test_create_post(self):
        user = User.objects.create(username="testuser")
        post = Post.objects.create(
            author=user,
            title_pl="Test Post",
            text_pl="This is a test post.",
            created_date=timezone.now(),
        )
        assert post.title_pl == "Test Post"
        assert post.text_pl == "This is a test post."
        assert post.published_date is None
        assert str(post) == "Test Post"

    def test_publish_post(self):
        user = User.objects.create(username="testuser")
        post = Post.objects.create(
            author=user,
            title_pl="Publish Test Post",
            text_pl="Publishing test post.",
            created_date=timezone.now(),
        )
        post.publish()
        assert post.published_date is not None
        assert post.published_date <= timezone.now()

    def test_delete_user_cascades_posts(self):
        user = User.objects.create(username="testuser")
        Post.objects.create(
            author=user,
            title_pl="Test Post",
            text_pl="This is a test post.",
            created_date=timezone.now(),
        )
        user.delete()
        assert Post.objects.count() == 0
