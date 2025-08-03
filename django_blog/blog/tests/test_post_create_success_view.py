import pytest
from django.urls import reverse

from accounts.models import UserAccount
from blog.models import Post


@pytest.mark.django_db
class TestPostCreateSuccessView:

    @pytest.fixture
    def user_and_post(self):
        user = UserAccount.objects.create_user(username="testuser", password="pass")
        post = Post.objects.create(
            title="Article test",
            slug="article-test",
            author=user,
            content="Contenu test",
            is_published=True,
        )
        return user, post

    def test_success_view_shows_published_message(self, client, user_and_post):
        user, post = user_and_post
        client.login(username="testuser", password="pass")
        url = reverse("blog:post_create_success") + f"?id={post.id}&action=create"
        response = client.get(url)
        assert response.status_code == 200
        html = response.content.decode("utf-8")
        assert "Article créé et publié avec succès" in html
        assert "create" in response.context["action"]

    def test_success_view_shows_draft_message(self, client, user_and_post):
        user, post = user_and_post
        post.is_published = False
        post.save()
        client.login(username="testuser", password="pass")
        url = reverse("blog:post_create_success") + f"?id={post.id}&action=update"
        response = client.get(url)
        assert response.status_code == 200
        html = response.content.decode("utf-8")
        assert "Brouillon enregistré" in html or "Brouillon mis à jour" in html
        assert "update" in response.context["action"]
