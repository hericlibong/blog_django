from django.shortcuts import get_object_or_404, render

from .models import UserProfile


def user_profile_view(request):
    """Vue pour afficher le profil utilisateur"""
    profile = get_object_or_404(UserProfile, user=request.user)
    return render(request, "accounts/profile.html", {"profile": profile})
