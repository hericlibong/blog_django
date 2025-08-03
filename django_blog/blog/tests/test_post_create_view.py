import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from accounts.models import UserAccount
from blog.models import Category, Post


@pytest.mark.django_db
class TestPostCreateView:

    @pytest.fixture
    def user(self):
        return UserAccount.objects.create_user(username="creator", password="pass")

    def test_access_create_view_authenticated(self, client, user):
        client.login(username="creator", password="pass")
        url = reverse("blog:post_create")
        response = client.get(url)
        assert response.status_code == 200
        assert "Créer un article" in response.content.decode()

    def test_create_post_draft(self, client, user):
        client.login(username="creator", password="pass")
        category = Category.objects.create(name="TestCat", slug="testcat")
        image = SimpleUploadedFile(
            "test.jpg",
            b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\xff\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x4c\x01\x00\x3b",
            content_type="image/gif",
        )

        url = reverse("blog:post_create")
        data = {
            "title": "Nouveau brouillon",
            "slug": "nouveau-brouillon",
            "content": "Contenu test",
            "image": image,
            "category": [category.id],
            "action": "draft",
        }

        response = client.post(url, data)
        assert response.status_code == 302
        assert Post.objects.filter(title="Nouveau brouillon").exists()

    def test_create_post_published(self, client, user):
        client.login(username="creator", password="pass")
        category = Category.objects.create(name="TestCat2", slug="testcat2")
        image = SimpleUploadedFile(
            "test.jpg",
            b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\xff\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x4c\x01\x00\x3b",
            content_type="image/gif",
        )

        url = reverse("blog:post_create")
        data = {
            "title": "Article publié",
            "slug": "article-publie",
            "content": "Contenu test",
            "image": image,
            "category": [category.id],
            "action": "publish",
        }

        response = client.post(url, data)
        assert response.status_code == 302
        assert Post.objects.get(slug="article-publie").is_published is True
