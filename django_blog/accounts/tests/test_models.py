import pytest

from accounts.models import UserAccount, UserProfile


@pytest.mark.django_db
def test_user_profile_str():
    """Vérifie la méthode __str__ du modèle UserProfile."""
    user = UserAccount.objects.create(username="testuser")
    profile = UserProfile.objects.create(user=user, short_bio="Développeur Python")

    assert str(profile) == f"Profile for {profile.user.username}"


@pytest.mark.django_db
def test_get_skills_list():
    """Vérifie que get_skills_list() retourne une liste propre."""
    user = UserAccount.objects.create(username="testuser")
    profile = UserProfile.objects.create(user=user, skills="Python, Django, REST API,  ")

    assert profile.get_skills_list() == ["Python", "Django", "REST API"]


@pytest.mark.django_db
def test_create_user_profile():
    """Vérifie qu'un UserProfile peut être créé avec des valeurs facultatives vides."""
    user = UserAccount.objects.create(username="testuser")
    profile = UserProfile.objects.create(user=user)  # Aucun champ facultatif rempli

    assert profile.bio is None
    assert profile.skills == ""
    assert profile.avatar is None
    assert profile.github is None
