import pytest
from django.utils import timezone
from django.utils.text import slugify

from blog.models import Category, Post, Tag


@pytest.mark.django_db
class TestCategoryModel:
    def test_str_representation(self):
        """Test the string representation of the Category model."""
        cat = Category.objects.create(name="Python", slug="python")
        assert str(cat) == "Python"

    def test_verbose_plural(self):
        """Test the verbose name plural of the Category model."""
        assert Category._meta.verbose_name_plural == "Categories"


@pytest.mark.django_db
class TestTagModel:
    def test_str_representation(self):
        """Test the string representation of the Tag model."""
        tag = Tag.objects.create(name="web")
        assert str(tag) == "web"


@pytest.mark.django_db
class TestPostModel:
    def test_str_representation(self, django_user_model):
        """Test the string representation of the Post model."""
        user = django_user_model.objects.create_user(username="testuser", password="pass")
        post = Post.objects.create(
            title="Article test", slug="article-test", author=user, content="du contenu"
        )
        assert str(post) == "Article test"

    def test_slug_auto_generated_if_missing(self, django_user_model):
        """Test that the slug is auto-generated if not provided."""
        user = django_user_model.objects.create_user(username="slugtest", password="pass")
        post = Post(title="Titre auto slug", author=user, content="du contenu")
        post.save()
        assert post.slug == slugify("Titre auto slug")

    def test_add_category_and_tags(self, django_user_model):
        """Test adding categories and tags to a post."""
        user = django_user_model.objects.create_user(username="reltest", password="pass")
        cat = Category.objects.create(name="Django", slug="django")
        tag1 = Tag.objects.create(name="dev")
        tag2 = Tag.objects.create(name="framework")

        post = Post.objects.create(
            title="Avec relations", slug="avec-rel", author=user, content="texte"
        )
        post.category.add(cat)
        post.tags.add(tag1, tag2)

        assert cat in post.category.all()
        assert tag1 in post.tags.all()
        assert tag2 in post.tags.all()

    def test_post_ordering(self, django_user_model):
        """Test the ordering of posts by created_at."""
        user = django_user_model.objects.create_user(username="orderuser", password="pass")
        Post.objects.create(
            title="Un", slug="un", author=user, content="...", created_at=timezone.now()
        )
        Post.objects.create(
            title="Deux", slug="deux", author=user, content="...", created_at=timezone.now()
        )

        posts = Post.objects.all()
        assert list(posts) == list(posts.order_by("-created_at"))
