import pytest
from portfolio.models import Project
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestProjectDetailView:
    """Test for ProjecDetailView"""

    @pytest.fixture
    def superuser(db):
        """fixturee to create a superuser"""
        return User.objects.create_superuser(username='admin', password='admin')

    @pytest.fixture
    def project(db, superuser, sample_image):
        """Fixture to create a sample project."""
        return Project.objects.create(
            title='Sample Project',
            description='Description for the sample project',
            created_by=superuser,
            image=sample_image
        )

    # Tester si la vue renvoie le code 200
    def test_detail_view_status_code(self, client, project):
        url = reverse('portfolio:project_detail', args=[project.id])
        response = client.get(url)
        assert response.status_code == 200

    def test_detail_view_404(self, client):
        """Test that the view returns a 404 status code for a non-existent project."""
        url = reverse('portfolio:project_detail', args=[999])  # ID inexistant
        response = client.get(url)
        assert response.status_code == 404

    def test_detail_view_template(self, client, project):
        """Test that the correct template is used."""
        url = reverse('portfolio:project_detail', args=[project.id])
        response = client.get(url)
        assert response.status_code == 200
        assert 'portfolio/project_detail.html' in [t.name for t in response.templates]

    def test_detail_view_context(self, client, project):
        """Test that the context contains the correct project."""
        url = reverse('portfolio:project_detail', args=[project.id])
        response = client.get(url)
        assert response.status_code == 200
        assert 'project' in response.context
        assert response.context['project'] == project