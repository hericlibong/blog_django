import pytest
from django.urls import reverse

from accounts.models import UserAccount
from blog.models import Post


@pytest.mark.django_db
class TestPostDeleteView:

    @pytest.fixture
    def post_setup(self):
        author = UserAccount.objects.create_user(username="author", password="pass")
        stranger = UserAccount.objects.create_user(username="stranger", password="pass")
        post = Post.objects.create(
            title="Post à supprimer",
            slug="post-supprimer",
            author=author,
            content="Contenu test",
            is_published=True
        )
        return author, stranger, post

    def test_author_can_delete_post(self, client, post_setup):
        author, _, post = post_setup
        client.login(username="author", password="pass")
        url = reverse("blog:post_delete", kwargs={"slug": post.slug})
        response = client.post(url)
        assert response.status_code == 302  # redirection
        assert not Post.objects.filter(id=post.id).exists()

    def test_stranger_cannot_delete_post(self, client, post_setup):
        _, stranger, post = post_setup
        client.login(username="stranger", password="pass")
        url = reverse("blog:post_delete", kwargs={"slug": post.slug})
        response = client.post(url)
        assert response.status_code == 404
        assert Post.objects.filter(id=post.id).exists()
