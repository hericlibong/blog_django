import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from portfolio.models import Project, ImageFolio

User = get_user_model()


@pytest.mark.django_db  # Active la base de données Django pour ce test
class TestProjectModel:
    """Test module for Project model using pytest."""

    @pytest.fixture
    def superuser(self):
        """Fixture to create a superuser."""
        return User.objects.create_superuser(username='admin', password='admin')

    @pytest.fixture
    def project(self, superuser):
        """Fixture to create a project."""
        return Project.objects.create(
            title='Test project',
            description='This is a test project',
            created_by=superuser
        )

    def test_project_creation(self, project, superuser):
        """Test the creation of a project."""
        assert project.title == 'Test project'
        assert project.description == 'This is a test project'
        assert project.created_by == superuser
        assert project.created_at is not None

    def test_project_str(self, project):
        """Test the string representation of a project."""
        assert str(project) == 'Test project'

    @pytest.mark.parametrize("title, valid", [
        ("Valid title", True),
        ("", False),  # Titre vide
        ("A" * 256, False),  # Titre trop long
    ])
    def test_project_title_validation(self, title, valid, superuser):
        """Test the validation of the project title."""
        project = Project(title=title, description="Test description", created_by=superuser)
        if valid:
            project.full_clean()  # Valide le modèle
            assert project.title == title

        else:
            with pytest.raises(ValidationError):
                project.full_clean()


@pytest.mark.django_db
class TestImageFolioModel:
    """Test module for ImageFolio model using pytest."""

    @pytest.fixture
    def superuser(self):
        """Fixture to create a superuser."""
        return User.objects.create_superuser(username='admin', password='admin')

    @pytest.fixture
    def project(self, superuser):
        """Fixture to create a project."""
        return Project.objects.create(
            title='Test project',
            description='This is a test project',
            created_by=superuser
        )

    @pytest.fixture
    def image_imagefolio_creation(self, project):
        """Fixture to create an image."""
        imagefolio = ImageFolio.objects.create(
            project=project,
            image='project_images/test.jpg',
            alt_text='Test image',
        )
        assert imagefolio.project == project
        assert imagefolio.image == 'project_images/test.jpg'
        assert imagefolio.alt_text == 'Test image'
        assert imagefolio.created_at is not None

    def test_imagefolio_str(self, project):
        """Test the string representation of an imagefolio."""
        imagefolio = ImageFolio(project=project, image='project_images/test.jpg', alt_text='Test image')
        assert str(imagefolio) == f"Image for project: {project.title}"
