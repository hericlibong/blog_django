from django.shortcuts import render, get_object_or_404
from .models import UserProfile


def user_profile_view(request):
    """ Vue pour afficher le profil utilisateur """
    profile = get_object_or_404(UserProfile, user=request.user)
    return render(request, 'accounts/profile.html', {'profile': profile})
