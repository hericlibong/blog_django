import openai
import requests
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



def chatbot_view(request):
    """ Vue pour le chatbot """
    return render(request, 'openaichat/chatbot.html')

def chatbot_response(request):
    """ Vue pour la réponse du chatbot à partir de l'API OpenAI """
    if request.method == 'POST':
        user_message = request.POST.get("message", "").lower().strip()
        
        if not user_message:
            return JsonResponse({'error': 'Aucun message reçu.'}, status=400)
        
        # Vérifier si le message de l'utilisateur correspond à une réponse prédéfinie
        for key, response in PREDIFINED_RESPONSES.items():
            if key in user_message:
                return JsonResponse({'response': response}, status=200)

        if not OPENAI_API_KEY:
            return JsonResponse({'error': 'Clé API OpenAI non trouvée. Vérifiez votre configuration.'}, status=500)

        try:
            client = openai.OpenAI(api_key=OPENAI_API_KEY)  # On passe explicitement la clé API
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": user_message}],
                max_tokens=100
            )
            bot_reply = response.choices[0].message.content
            return JsonResponse({'response': bot_reply}, status=200)
        except openai.OpenAIError as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Méthode non autorisée.'}, status=405)

