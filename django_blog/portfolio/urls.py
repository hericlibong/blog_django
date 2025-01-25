from django.urls import path
from .views import ProjectListView

app_name = 'portfolio'

urlpatterns = [
    path('projects/', ProjectListView.as_view(), name='project_list'),
]
