from django.shortcuts import render
from .models import Project
from django.views.generic import ListView, DetailView


class ProjectListView(ListView):
    model = Project
    template_name = 'portfolio/project_list.html'
    context_object_name = 'projects'
