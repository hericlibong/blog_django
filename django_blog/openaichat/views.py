import openai
from decouple import config
from django.http import JsonResponse
from django.shortcuts import render

from accounts.models import UserProfile
from blog.models import Post
from portfolio.models import Project

# Récupérer explicitement la clé API
OPENAI_API_KEY = config("OPENAI_API_KEY", default=None)


def get_blog_context():
    posts = Post.objects.filter(is_published=True).order_by("-created_at")
    if not posts:
        return "Aucun article n'a encore été publié sur le blog.\n"
    summary = []
    for post in posts[:5]:
        snippet = post.subtitle or post.content[:100]
        summary.append(f"- **{post.title}** : {snippet}")
    return "**Derniers articles publiés sur le blog :**\n" + "\n".join(summary) + "\n"


def get_portfolio_context():
    """Fonction pour récupérer le contexte du portfolio"""
    projects = Project.objects.all()
    if not projects:
        return "les portfolio ne contient pas de projet pour le moment"

    project_summaries = "\n".join([f"- **{p.title}** : {p.description[:100]}..." for p in projects])
    return f"**Liste des projets de HericLdev :**\n{project_summaries}\n"


def get_user_profile():
    profile = UserProfile.objects.first()
    if not profile:
        return "Aucune information de profil disponible."
    return (
        f"**Biographie** : {profile.bio}\n"
        f"**Compétences** : {profile.skills}\n"
        f"**Expérience** : {profile.experience}\n"
        f"**GitHub** : {profile.github}\n"
        f"**LinkedIn** : {profile.linkedin}\n"
    )


def chatbot_view(request):
    """Vue pour le chatbot"""
    return render(request, "openaichat/chatbot.html")


def chatbot_response(request):
    """Vue pour la réponse du chatbot avec un contexte dynamique enrichi"""
    if request.method == "POST":
        user_message = request.POST.get("message", "").lower().strip()

        if not user_message:
            return JsonResponse({"error": "Aucun message reçu."}, status=400)

        # Contexte mis à jour avec le profil et les projets
        CONTEXT = f"""
        Tu es un assistant personnel pour le portfolio de HericLdev.
        Présente toujours les listes (projets, articles, compétences…) sous forme de puces ou de listes numérotées,
        avec les titres des éléments en gras (**titre**), et chaque élément sur une ligne séparée.
        Utilise du markdown si nécessaire pour la lisibilité.

        **Profil** :
        {get_user_profile()}

        **Projets** :
        {get_portfolio_context()}

        **Articles de blog** :
        {get_blog_context()}
        """
        if not OPENAI_API_KEY:
            return JsonResponse(
                {"error": "Clé API OpenAI non trouvée. Vérifiez votre configuration."}, status=500
            )
        try:
            client = openai.OpenAI(api_key=OPENAI_API_KEY)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": CONTEXT},
                    {"role": "user", "content": user_message},
                ],
                max_tokens=500,
            )
            bot_reply = response.choices[0].message.content
            return JsonResponse({"response": bot_reply}, status=200)
        except openai.OpenAIError as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Méthode non autorisée."}, status=405)
