from django.shortcuts import render, get_object_or_404
from .models import UserProfile
from django.contrib.auth.decorators import login_required


@login_required
def user_profile_view(request):
    """ Vue pour afficher le profil utilisateur """
    profile = get_object_or_404(UserProfile, user=request.user)
    return render(request, 'accounts/profile.html', {'profile': profile})


