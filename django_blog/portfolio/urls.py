from django.urls import path
from .views import ProjectListView, ProjectDetailView, AboutView

app_name = 'portfolio'

urlpatterns = [
    path('projects/', ProjectListView.as_view(), name='project_list'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
     path('about/', AboutView.as_view(), name='about'),
]
