from django.db import models
from django.contrib.auth.models import AbstractUser


class UserAccount(AbstractUser):
    """Custom user model for accounts."""
    pass
