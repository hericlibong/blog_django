import pytest
from django.urls import reverse

from accounts.models import UserAccount
from blog.models import Category, Post, Tag


@pytest.mark.django_db
class TestPostListView:

    @pytest.fixture
    def setup_data(self):
        user = UserAccount.objects.create_user(username="author", password="pass", is_staff=True)
        other = UserAccount.objects.create_user(username="visitor", password="pass")

        cat = Category.objects.create(name="Python", slug="python")
        tag = Tag.objects.create(name="dev")

        post1 = Post.objects.create(
            title="Publié", slug="publie", author=user, is_published=True, content="ok"
        )
        post1.category.add(cat)
        post1.tags.add(tag)

        post2 = Post.objects.create(
            title="Brouillon", slug="draft", author=user, is_published=False, content="draft"
        )
        post2.category.add(cat)

        return user, other, cat, tag, post1, post2

    def test_anonymous_user_sees_only_published(self, client, setup_data):
        url = reverse("blog:post_list")
        response = client.get(url)

        assert response.status_code == 200
        html = response.content.decode("utf-8")
        assert "Publié" in html
        assert "Brouillon" not in html

    def test_staff_user_sees_all_own_posts(self, client, setup_data):
        user, *_ = setup_data
        client.login(username="author", password="pass")
        url = reverse("blog:post_list")
        response = client.get(url)

        html = response.content.decode("utf-8")
        assert "Publié" in html
        assert "Brouillon" in html

    def test_filter_by_category(self, client, setup_data):
        _, _, cat, _, post1, _ = setup_data
        url = reverse("blog:post_list") + f"?category={cat.slug}"
        response = client.get(url)

        assert response.status_code == 200
        html = response.content.decode("utf-8")
        assert post1.title in html

    def test_filter_by_tag(self, client, setup_data):
        _, _, _, tag, post1, _ = setup_data
        url = reverse("blog:post_list") + f"?tag={tag.name}"
        response = client.get(url)

        assert response.status_code == 200
        html = response.content.decode("utf-8")
        assert post1.title in html

    def test_filter_by_status_published(self, client, setup_data):
        user, *_ = setup_data
        client.login(username="author", password="pass")
        url = reverse("blog:post_list") + "?filter=published"
        response = client.get(url)

        assert response.status_code == 200
        html = response.content.decode("utf-8")
        assert "Publié" in html

    def test_filter_by_status_draft(self, client, setup_data):
        user, *_ = setup_data
        client.login(username="author", password="pass")
        url = reverse("blog:post_list") + "?filter=draft"
        response = client.get(url)

        assert response.status_code == 200
        assert "Brouillon" in str(response.content)
        assert "Publié" not in str(response.content)
