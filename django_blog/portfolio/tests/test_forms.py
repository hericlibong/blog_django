import pytest
from django_ckeditor_5.widgets import CKEditor5Widget

from portfolio.forms import ProjectForm


@pytest.mark.django_db
class TestProjectForm:
    """Tests for the ProjectForm form."""

    def test_valid_form(self):
        """Test that the form is valid with correct data."""
        data = {
            "title": "Test project",
            "description": "This is a test project",
        }
        form = ProjectForm(data=data)
        assert form.is_valid()

    def test_invalid_title(self):
        """Test that the form is invalid if the title is too short."""
        data = {
            "title": "Tes",
            "description": "This is a test project description",
        }
        form = ProjectForm(data=data)
        assert not form.is_valid()
        assert "title" in form.errors
        assert form.errors["title"] == ["Le titre doit contenir au moins 5 caractères."]

    def test_empty_description(self):
        """Test that the form is invalid if the description is empty."""
        data = {
            "title": "Test project",
            "description": "",
        }
        form = ProjectForm(data=data)
        assert not form.is_valid()
        assert "description" in form.errors

    def test_widget_configuration(self):
        """Test that widgets are properly configured."""
        form = ProjectForm()
        assert form.fields["title"].widget.attrs["class"] == "form-control"
        assert isinstance(form.fields["description"].widget, CKEditor5Widget)

    def test_clean_title_method(self):
        """Test the clean_title method."""
        form = ProjectForm(data={"title": "Test", "description": "Description valide."})
        assert not form.is_valid()  # Validation échoue
        assert "title" in form.errors
