from django.db import models
from django.contrib.auth import get_user_model
from cloudinary.models import CloudinaryField
from ckeditor.fields import RichTextField


User = get_user_model()


class Project(models.Model):
    """Model definition for Project."""
    title = models.CharField(max_length=255, unique=True)
    description = RichTextField(max_length=5000, help_text="Full text of the project")
    image = CloudinaryField("image", folder="project_images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self):
        return self.title


class ImageFolio(models.Model):
    """Model definition for Image."""
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="project_images/", blank=True, null=True)
    alt_text = models.CharField(max_length=255, blank=True, help_text="Texte alternatif pour l'image")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"

    def __str__(self):
        return f"Image for project: {self.project.title}"
