import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestAboutView:
    """Tests for the AboutView."""

    def test_about_view_status_code(self, client):
        """Test that the about page returns a 200 status code."""
        url = reverse('portfolio:about')
        response = client.get(url)
        assert response.status_code == 200

    def test_about_view_template(self, client):
        """Test that the correct template is used."""
        url = reverse('portfolio:about')
        response = client.get(url)
        assert response.status_code == 200
        assert 'portfolio/about.html' in [t.name for t in response.templates]
