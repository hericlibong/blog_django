from django.shortcuts import render
from .models import Project
from django.views.generic import ListView, DetailView, TemplateView



class ProjectListView(ListView):
    model = Project
    template_name = 'portfolio/project_list.html'
    context_object_name = 'projects'


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'portfolio/project_detail.html'
    context_object_name = 'project'


class AboutView(TemplateView):
    template_name = 'portfolio/about.html'
