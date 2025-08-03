import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from accounts.models import UserAccount
from blog.models import Category, Post


@pytest.mark.django_db
class TestPostUpdateView:

    @pytest.fixture
    def setup_post(self):
        author = UserAccount.objects.create_user(username="author", password="pass", is_staff=True)
        stranger = UserAccount.objects.create_user(username="stranger", password="pass")
        category = Category.objects.create(name="TestCat", slug="testcat")
        post = Post.objects.create(
            title="Titre original",
            slug="titre-original",
            content="Ancien contenu",
            author=author,
            is_published=False,
        )
        post.category.add(category)
        return author, stranger, post

    def test_author_can_access_update_view(self, client, setup_post):
        author, _, post = setup_post
        client.login(username="author", password="pass")
        url = reverse("blog:post_update", kwargs={"slug": post.slug})
        response = client.get(url)
        assert response.status_code == 200
        assert "Modifier un article" in response.content.decode()

    def test_author_can_update_post(self, client, setup_post):
        author, _, post = setup_post
        client.login(username="author", password="pass")
        image = SimpleUploadedFile(
            "test.jpg",
            b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\xff\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x4c\x01\x00\x3b",
            content_type="image/gif",
        )

        url = reverse("blog:post_update", kwargs={"slug": post.slug})
        data = {
            "title": "Titre modifié",
            "slug": "titre-modifie",
            "content": "Nouveau contenu",
            "image": image,
            "category": [cat.id for cat in post.category.all()],
            "action": "draft",
        }
        response = client.post(url, data)
        assert response.status_code == 302
        post.refresh_from_db()
        assert post.title == "Titre modifié"

    def test_author_can_publish_from_update(self, client, setup_post):
        author, _, post = setup_post
        client.login(username="author", password="pass")
        url = reverse("blog:post_update", kwargs={"slug": post.slug})
        data = {
            "title": post.title,
            "slug": post.slug,
            "content": post.content,
            "image": SimpleUploadedFile(
                "test.jpg",
                b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\xff\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x4c\x01\x00\x3b",
                content_type="image/gif",
            ),
            "category": [cat.id for cat in post.category.all()],
            "action": "publish",
        }
        response = client.post(url, data)
        post.refresh_from_db()
        assert response.status_code == 302
        assert post.is_published

    def test_non_author_gets_403_or_404(self, client, setup_post):
        _, stranger, post = setup_post
        client.login(username="stranger", password="pass")
        url = reverse("blog:post_update", kwargs={"slug": post.slug})
        response = client.get(url)
        assert response.status_code in [403, 404]

    def test_anonymous_user_redirected(self, client, setup_post):
        _, _, post = setup_post
        url = reverse("blog:post_update", kwargs={"slug": post.slug})
        response = client.get(url)
        assert response.status_code == 302
        assert "/login" in response.url
