import pytest
import shutil
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from pathlib import Path

@pytest.fixture(scope='session', autouse=True)
def set_up_media_root(tmp_path_factory):
    """Fixture to set up the media root."""
    media_root = tmp_path_factory.mktemp('media')
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
    