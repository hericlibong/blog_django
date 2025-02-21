import pytest
from django.test import Client
from openaichat.views import get_portfolio_context, get_user_profile
from portfolio.models import Project
from accounts.models import UserAccount, UserProfile
from django.urls import reverse
from unittest.mock import patch, MagicMock
import openai


@pytest.fixture
def client():
    """Fixture pour initialiser un client Django."""
    return Client()


# Tester 'get_portfolio_context()
@pytest.mark.django_db
def test_get_portfolio_context_no_projects():
    """Teste la réponse quand il n'y a pas de projet."""
    assert get_portfolio_context() == "les portfolio ne contient pas de projet pour le moment"


@pytest.mark.django_db
def test_get_portfolio_context_with_projects():
    """Teste la réponse avec des projets."""

    # Créer un utilisateur d'abord
    user = UserAccount.objects.create_user(username="testuser", password="testpassword")
    user.save()  # Force l'enregistrement de l'utilisateur en base pour générer un ID

    # Associer les projets à cet utilisateur
    Project.objects.create(title='Project 1', description='Description for project 1', created_by_id=user.id)
    Project.objects.create(title='Project 2', description='Description for project 2', created_by_id=user.id)

    result = get_portfolio_context()

    # Vérifier que les projets sont bien inclus dans la réponse
    assert "Project 1" in result
    assert "Project 2" in result


@pytest.mark.django_db
def test_get_user_profile_no_profile():
    """Teste la réponse quand il n'y a pas de profil utilisateur."""
    assert get_user_profile() == "Aucune information de profil disponible."


@pytest.mark.django_db
def test_get_user_profile_with_profile():
    """Teste la réponse quand un profil utilisateur existe"""
    user = UserAccount.objects.create(username="testuser")
    UserProfile.objects.create(user=user, bio="Développeur Python", skills="Python, Django")

    result = get_user_profile()
    assert "Développeur Python" in result
    assert "Python, Django" in result


@pytest.mark.django_db
def test_chatbot_view(client):
    """Teste si la page chatbot est accessible"""
    response = client.get(reverse("openaichat:chatbot"))
    assert response.status_code == 200
    assert "openaichat/chatbot.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_chatbot_response_success(client):
    """Teste une requête valide au chatbot"""
    with patch("openai.OpenAI.chat.completions.create") as mock_openai:
        mock_openai.return_value = MagicMock(choices=[MagicMock(message=MagicMock(content="Réponse test"))])

        response = client.post(reverse("openaichat:chatbot_response"), {"message": "Bonjour"})
        assert response.status_code == 200
        assert "Réponse test" in response.json()["response"]


@pytest.mark.django_db
def test_chatbot_response_empty_message(client):
    """Teste si un message vide retourne une erreur 400"""
    response = client.post(reverse("openaichat:chatbot_response"), {"message": ""})
    assert response.status_code == 400
    assert "Aucun message reçu" in response.json()["error"]


@pytest.mark.django_db
@patch("openai.OpenAI")
def test_chatbot_response_successul(mock_openai, client):
    mock_instance = mock_openai.return_value
    mock_instance.chat.completions.create.return_value = MagicMock(choices=[MagicMock(message=MagicMock(content="Réponse test"))])

    response = client.post(reverse('openaichat:chatbot_response'), {"message": "Bonjour"})
    assert response.status_code == 200
    assert response.json()["response"] == "Réponse test"


@pytest.mark.django_db
@patch("openai.OpenAI")
def test_chatbot_response_api_error(mock_openai, client):
    mock_instance = mock_openai.return_value
    mock_instance.chat.completions.create.side_effect = openai.OpenAIError("Erreur API")

    response = client.post(reverse('openaichat:chatbot_response'), {"message": "Erreur test"})
    assert response.status_code == 500
    assert "Erreur API" in response.json()["error"]


def test_chatbot_response_invalid_method(client):
    """Vérifie qu'une requête GET renvoie une erreur 405 (Méthode non autorisée)."""
    response = client.get(reverse('openaichat:chatbot_response'))
    assert response.status_code == 405
    assert response.json()["error"] == "Méthode non autorisée."
