import pytest
from django.urls import reverse
from portfolio.models import Project
from django.contrib.auth import get_user_model
from portfolio.forms import ProjectForm

User = get_user_model()


@pytest.mark.django_db
class TestProjectUpdateView:
    """Tests for the ProjectUpdateView."""

    @pytest.fixture
    def superuser(self):
        """Fixture to create a superuser."""
        return User.objects.create_superuser(username='admin', password='admin')

    @pytest.fixture
    def project(self, superuser):
        """Fixture to create a sample project."""
        return Project.objects.create(
            title='Original Title',
            description='Original description',
            created_by=superuser
        )

    def test_update_view_status_code(self, client, superuser, project):
        """Test that the update page returns a 200 status code."""
        client.force_login(superuser)
        url = reverse('portfolio:project_update', args=[project.id])
        response = client.get(url)
        assert response.status_code == 200
        assert 'portfolio/project_form.html' in [t.name for t in response.templates]

    def test_update_view_404(self, client, superuser):
        """Test that accessing a non-existent project returns a 404."""
        client.force_login(superuser)
        url = reverse('portfolio:project_update', args=[999])  # ID inexistant
        response = client.get(url)
        assert response.status_code == 404

    def test_update_project_valid_data(self, client, superuser, project):
        """Test that valid data updates the project."""
        client.force_login(superuser)
        url = reverse('portfolio:project_update', args=[project.id])
        data = {
            'title': 'Updated Title',
            'description': 'Updated description',
        }
        response = client.post(url, data)
        assert response.status_code == 302  # Redirection après succès
        assert response.url == reverse('portfolio:project_list')  # Redirige vers la liste des projets
        project.refresh_from_db()  # Recharge les données depuis la BDD
        assert project.title == 'Updated Title'
        assert project.description == 'Updated description'

    def test_update_project_invalid_data(self, client, superuser, project):
        """Test that invalid data does not update the project."""
        client.force_login(superuser)
        url = reverse('portfolio:project_update', args=[project.id])
        data = {
            'title': '',  # Titre vide (invalide)
            'description': '',
        }
        response = client.post(url, data)
        project.refresh_from_db()
        assert response.status_code == 200  # Reste sur la page avec erreurs
        assert 'form' in response.context
        assert response.context['form'].errors  # Vérifie qu'il y a des erreurs
        assert project.title == 'Original Title'  # Le titre ne doit pas avoir changé

    def test_update_project_redirect(self, client, superuser, project):
        """Test that updating a project redirects to the project list."""
        client.force_login(superuser)
        url = reverse('portfolio:project_update', args=[project.id])
        data = {
            'title': 'Updated Title',
            'description': 'Updated description',
        }
        response = client.post(url, data)
        assert response.status_code == 302
        assert response.url == reverse('portfolio:project_list')

    def test_update_view_contains_form(self, client, superuser, project):
        client.force_login(superuser)
        url = reverse('portfolio:project_update', args=[project.id])
        response = client.get(url)
        assert 'form' in response.context
        assert isinstance(response.context['form'], ProjectForm)
