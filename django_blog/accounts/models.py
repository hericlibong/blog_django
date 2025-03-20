from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField


class UserAccount(AbstractUser):
    """Custom user model for accounts."""
    pass


class UserProfile(models.Model):
    """Model definition for UserProfile."""
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
    short_bio = models.CharField(max_length=400, blank=True, null=True, help_text="Your short bio for the template profile")
    bio = models.TextField(blank=True, null=True, help_text="Your bio")
    experience = models.TextField(blank=True, help_text="Your professional experience")
    skills = models.TextField(blank=True, help_text="Your skills")
    avatar = CloudinaryField("image", folder="profile_avatars/", blank=True, null=True)
    github = models.URLField(blank=True, null=True, help_text="Your GitHub profile")
    linkedin = models.URLField(blank=True, null=True, help_text="Your LinkedIn profile")
    website = models.URLField(blank=True, null=True, help_text="Your personal website")
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "UserProfile"
        verbose_name_plural = "UserProfiles"

    def __str__(self):
        return f"Profile for {self.user.username}"

    def get_skills_list(self):
        """Retourne une liste de compétences à partir de la chaîne de caractères, séparées par des virgules."""
        return [skill.strip() for skill in self.skills.split(",") if skill.strip()]
