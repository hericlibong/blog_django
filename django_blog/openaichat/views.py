import openai
import requests
from accounts.models import UserAccount, UserProfile
from portfolio.models import Project
from django.shortcuts import render
from django.http import JsonResponse
from decouple import config
import os
import json



# Récupérer explicitement la clé API
OPENAI_API_KEY = config('OPENAI_API_KEY', default=None)

# Chemin vers le fichier json contenant les réponses du chatbot
RESPONSES_FILE = os.path.join(os.path.dirname(__file__), 'responses.json')


# Fonction pour charger les réponses du chatbot à partir du fichier json
def load_responses():
    try:
        with open(RESPONSES_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

PREDIFINED_RESPONSES = load_responses()    

def get_portfolio_context():
    """ Fonction pour récupérer le contexte du portfolio """
    projects = Project.objects.all()
    if not projects:
        return "les portfolio ne contient pas de projet pour le moment"

    project_summaries = "\n".join([f"{p.title}: {p.description[:100]}..." for p in projects])
    return f"Voici une liste des projets de HericLdev :\n{project_summaries}\n"

def get_user_profile():
    """ Récupère les informations du profil utilisateur pour le chatbot """
    profile = UserProfile.objects.first()  # Supposons qu'il n'y a qu'un seul profil
    if not profile:
        return "Aucune information de profil disponible."

    return f"""
    Biographie : {profile.bio}
    Compétences : {profile.skills}
    short bio : {profile.short_bio}
    Expérience : {profile.experience}
    GitHub : {profile.github}
    LinkedIn : {profile.linkedin}
    """

def chatbot_view(request):
    """ Vue pour le chatbot """
    return render(request, 'openaichat/chatbot.html')

def chatbot_response(request):
    """ Vue pour la réponse du chatbot avec un contexte dynamique enrichi """
    if request.method == 'POST':
        user_message = request.POST.get("message", "").lower().strip()
        
        if not user_message:
            return JsonResponse({'error': 'Aucun message reçu.'}, status=400)

        # Contexte mis à jour avec le profil et les projets
        CONTEXT = f"""
        Tu es un assistant personnel pour le portfolio de HericLdev.
        Voici des informations sur son profil :
        {get_user_profile()}

        Et voici ses projets :
        {get_portfolio_context()}
        
        Réponds de manière claire et informative en fonction de ces informations.
        """

        if not OPENAI_API_KEY:
            return JsonResponse({'error': 'Clé API OpenAI non trouvée. Vérifiez votre configuration.'}, status=500)

        try:
            client = openai.OpenAI(api_key=OPENAI_API_KEY)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": CONTEXT},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=150
            )
            bot_reply = response.choices[0].message.content
            return JsonResponse({'response': bot_reply}, status=200)
        except openai.OpenAIError as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Méthode non autorisée.'}, status=405)

