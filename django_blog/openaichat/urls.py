from django.urls import path

from .views import chatbot_response, chatbot_view

app_name = "openaichat"

urlpatterns = [
    path("chatbot/", chatbot_view, name="chatbot"),
    path("chatbot-response/", chatbot_response, name="chatbot_response"),
]
