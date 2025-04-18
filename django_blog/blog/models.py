from django.db import models
from cloudinary.models import CloudinaryField
from ckeditor.fields import RichTextField
from accounts.models import UserAccount


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    subtitle = models.CharField(max_length=300, blank=True, null=True)
    image = CloudinaryField("image", folder="blog_images/")
    content = RichTextField()
    author = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, related_name="posts")
    tags = models.ManyToManyField(Tag, blank=True, related_name="posts")
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
