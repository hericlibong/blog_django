import pytest
from portfolio.models import Project
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestProjectCreateView:
    """Test for ProjectCreateView"""

    @pytest.fixture
    def superuser(db):
        """Fixture to create a superuser."""
        return User.objects.create_superuser(username='admin', password='admin')
    
    def test_create_view_status_code(self, client, superuser):
        """Test that the view returns a 200 status code for GET requests."""
        client.force_login(superuser)  # Connecte le superuser
        url = reverse('portfolio:project_create')
        response = client.get(url)
        assert response.status_code == 200

    def test_create_project_valid_data(self, client, superuser):
        """Test that a project is created with valid data."""
        client.force_login(superuser)
        url = reverse('portfolio:project_create')
        data = {
            'title': 'New Project',
            'description': 'This is a new project',
            
        }
        response = client.post(url, data)
        assert response.status_code == 302  # Redirection après succès
        assert Project.objects.filter(title='New Project').exists()

    def test_create_project_invalid_data(self, client, superuser):
        """Test that invalid data does not create a project."""
        client.force_login(superuser)
        url = reverse('portfolio:project_create')
        data = {
            'title': '',  # Titre vide
            'description': '',
        }
        response = client.post(url, data)
        assert response.status_code == 200  # Reste sur la page avec des erreurs
        assert not Project.objects.filter(title='').exists()

    def test_create_project_no_superuser(self, client):
        """Test that trying to create a project without a superuser raises ValueError."""
        url = reverse('portfolio:project_create')
        data = {
            'title': 'Project Without Superuser',
            'description': 'This project should not be created',
        }
        
        with pytest.raises(ValueError, match="Aucun superutilisateur n'est défini. Créez un superutilisateur avant de continuer."):
            client.post(url, data)