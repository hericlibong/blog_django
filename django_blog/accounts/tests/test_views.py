import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models import UserProfile


User = get_user_model()


@pytest.mark.django_db
def test_user_profile_view_with_profile(client):
    """Vérifie que le profil est accessible et affiche les données."""
    # ✅ Création d'un utilisateur test
    user = User.objects.create_user(username="testuser", password="password123")

    # ✅ Création d'un profil lié à cet utilisateur
    # profile = UserProfile.objects.create(
    #     user=user,
    #     short_bio="Développeur Python"
    # )

    # ✅ Authentification du client test
    client.force_login(user)

    url = reverse("accounts:user_profile")  # Correction ici
    response = client.get(url)

    assert response.status_code == 200
    assert "Développeur Python" in response.content.decode()


@pytest.mark.django_db
def test_user_profile_view_no_profile(client):
    """Vérifie qu'une erreur 404 est retournée si aucun profil n'existe pour l'utilisateur."""
    # ✅ Création d'un utilisateur SANS profil
    user = User.objects.create_user(username="testuser", password="password123")

    # ✅ Authentification du client test
    client.force_login(user)

    url = reverse("accounts:user_profile")
    response = client.get(url)

    assert response.status_code == 404  # Aucun profil existant pour cet utilisateur
