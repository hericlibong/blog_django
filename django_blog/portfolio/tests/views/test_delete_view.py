from unittest.mock import patch

import pytest
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.urls import reverse

from portfolio.models import Project
from portfolio.views import ProjectDeleteView

User = get_user_model()


@pytest.mark.django_db
class TestProjectDeleteView:
    """Tests for the ProjectDeleteView."""

    @pytest.fixture
    def superuser(self):
        """Fixture to create a superuser."""
        return User.objects.create_superuser(username='admin', password='admin')

    @pytest.fixture
    def project(self, superuser):
        """Fixture to create a sample project."""
        return Project.objects.create(
            title='Project to Delete',
            description='This project will be deleted',
            created_by=superuser
        )

    def test_delete_view_status_code(self, client, superuser, project):
        """Test that the delete page returns a 200 status code."""
        client.force_login(superuser)
        url = reverse('portfolio:project_delete', args=[project.id])
        response = client.get(url)
        assert response.status_code == 200

    def test_delete_view_404(self, client, superuser):
        """Test that accessing a non-existent project returns a 404."""
        client.force_login(superuser)
        url = reverse('portfolio:project_delete', args=[999])  # ID inexistant
        response = client.get(url)
        assert response.status_code == 404

    def test_delete_project(self, client, superuser, project):
        """Test that deleting a project works correctly."""
        client.force_login(superuser)
        url = reverse('portfolio:project_delete', args=[project.id])
        response = client.post(url)
        assert response.status_code == 302  # Redirection après suppression
        assert not Project.objects.filter(id=project.id).exists()  # Vérifie la suppression

    def test_delete_project_calls_super_delete(self, client, superuser, project):
        """Test que la méthode delete de la classe parente est bien appelée."""
        client.force_login(superuser)

        # Créer une instance de la vue
        view = ProjectDeleteView()

        # Simuler les attributs nécessaires pour la vue
        request = HttpRequest()
        request.method = 'POST'
        request.user = superuser
        view.request = request
        view.kwargs = {'pk': project.id}  # Simuler les kwargs de l'URL
        view.object = project  # Définir l'objet à supprimer

        # Mock la méthode delete sur l'instance de la vue
        with patch.object(view, 'delete', wraps=view.delete) as mock_delete:
            # Appeler la méthode delete directement
            response = view.delete(request)

            # Vérifie que la méthode delete de la classe parente est appelée
            mock_delete.assert_called_once()

            # Vérifie que la réponse est une redirection après suppression
            assert response.status_code == 302

            # Vérifie que le projet est bien supprimé
            assert not Project.objects.filter(id=project.id).exists()
