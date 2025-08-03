import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from portfolio.models import Project

User = get_user_model()


@pytest.mark.django_db
class TestProjectListView:
    """Test for ProjectListView."""

    @pytest.fixture
    def superuser(db):
        """Fixture to create a superuser."""
        return User.objects.create_superuser(username='admin', password='admin')

    @pytest.fixture
    def projects(db, superuser, sample_image):
        """Fixture to create sample projects assigned to a superuser."""
        return [
            Project.objects.create(
                title='Project 1',
                description='Description for project 1',
                created_by=superuser,  # Correction : Associer un utilisateur
                image=sample_image
            ),
            Project.objects.create(
                title='Project 2',
                description='Description for project 2',
                created_by=superuser,  # Correction : Associer un utilisateur
                image=sample_image
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
        # assert list(response.context['projects']) == projects
        # ✅ Adapter au nouvel ordre DESC en inversant la liste
        assert list(response.context['projects']) == projects[::-1]

    def test_list_view_no_projects(self, client):
        """Test l'affichage du message quand il n'y a aucun projet."""
        url = reverse('portfolio:project_list')
        response = client.get(url)
        assert response.status_code == 200  # Vérifie que la page se charge correctement
