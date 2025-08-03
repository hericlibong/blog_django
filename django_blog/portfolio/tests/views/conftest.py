import shutil
from unittest.mock import patch

import pytest
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.fixture(scope="session", autouse=True)
def set_up_media_root(tmp_path_factory):
    """Fixture to set up the media root."""
    media_root = tmp_path_factory.mktemp("media")
    settings.MEDIA_ROOT = str(media_root)
    yield
    # Clean up after the tests
    shutil.rmtree(media_root)


@pytest.fixture
def sample_image():
    """
    Crée une image factice en mémoire pour les tests et retourne un fichier temporaire.
    """
    return SimpleUploadedFile("test_image.jpg", b"fake image data", content_type="image/jpeg")


@pytest.fixture(autouse=True)  # <-- Fixture globale pour tous les tests
def mock_cloudinary_upload():
    """Simule l'upload d'images vers Cloudinary."""
    with patch("cloudinary.uploader.upload_resource") as mock_upload:
        # Retourne une URL fictive pour l'image
        mock_upload.return_value = "https://res.cloudinary.com/fake/image.jpg"
        yield
