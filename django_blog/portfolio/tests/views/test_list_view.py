import pytest
from portfolio.models import Project
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()

@pytest.mark.django_db
class TestProjectListView:
    """Test for ProjectListView."""

    @pytest.fixture
    def superuser(db):
        """Fixture to create a superuser."""
        return User.objects.create_superuser(username='admin', password='admin')

    @pytest.fixture
    def projects(db, superuser):
        """Fixture to create sample projects assigned to a superuser."""
        test_image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")  
        return [
            Project.objects.create(
                title='Project 1',
                description='Description for project 1',
                created_by=superuser,  # Correction : Associer un utilisateur
                image = test_image
            ),
            Project.objects.create(
                title='Project 2',
                description='Description for project 2',
                created_by=superuser,  # Correction : Associer un utilisateur
                image = test_image
            ),
        ]

    # Tester si la vue renvoie le code 200
    def test_list_view_status_code(self, client):
        url = reverse('portfolio:project_list')
        response = client.get(url)
        assert response.status_code == 200

    # Tester si la vue utilise le bon template
    def test_list_view_template(self, client):
        url = reverse('portfolio:project_list')
        response = client.get(url)
        assert 'portfolio/project_list.html' in [t.name for t in response.templates]
    
    # Tester si la vue renvoie les projets
    def test_list_view_context(self, client, projects):
        url = reverse('portfolio:project_list')
        response = client.get(url)
        assert response.status_code == 200
        assert 'projects' in response.context
        assert list(response.context['projects']) == projects

    def test_list_view_no_projects(self, client):
        """Test l'affichage du message quand il n'y a aucun projet."""
        url = reverse('portfolio:project_list')
        response = client.get(url)
        assert response.status_code == 200  # Vérifie que la page se charge correctement
        assert "<li>Aucun projet disponible.</li>" in response.content.decode()  # Vérifie que le message est affiché
       