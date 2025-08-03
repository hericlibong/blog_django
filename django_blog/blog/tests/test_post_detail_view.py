import pytest
from django.urls import reverse

from accounts.models import UserAccount
from blog.models import Post


@pytest.mark.django_db
class TestPostDetailView:

    @pytest.fixture
    def detail_setup(self):
        author = UserAccount.objects.create_user(username="author", password="pass")
        stranger = UserAccount.objects.create_user(username="stranger", password="pass")

        published = Post.objects.create(
            title="Article publié",
            slug="article-publie",
            author=author,
            is_published=True,
            content="contenu publié"
        )

        draft = Post.objects.create(
            title="Brouillon",
            slug="brouillon",
            author=author,
            is_published=False,
            content="contenu caché"
        )

        return author, stranger, published, draft

    def test_detail_view_published_visible(self, client, detail_setup):
        _, _, published, _ = detail_setup
        url = reverse("blog:post_detail", kwargs={"slug": published.slug})
        response = client.get(url)
        html = response.content.decode("utf-8")
        assert response.status_code == 200
        assert published.title in html

    def test_draft_visible_by_author_only(self, client, detail_setup):
        author, _, _, draft = detail_setup
        client.login(username="author", password="pass")
        url = reverse("blog:post_detail", kwargs={"slug": draft.slug})
        response = client.get(url)
        html = response.content.decode("utf-8")
        assert response.status_code == 200
        assert draft.title in html

    def test_draft_hidden_from_others(self, client, detail_setup):
        _, stranger, _, draft = detail_setup
        client.login(username="stranger", password="pass")
        url = reverse("blog:post_detail", kwargs={"slug": draft.slug})
        response = client.get(url)
        assert response.status_code == 404

    def test_draft_hidden_from_anonymous(self, client, detail_setup):
        _, _, _, draft = detail_setup
        url = reverse("blog:post_detail", kwargs={"slug": draft.slug})
        response = client.get(url)
        assert response.status_code == 404
