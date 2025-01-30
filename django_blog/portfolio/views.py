from django.shortcuts import render
from .models import Project
from .forms import ProjectForm
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

User = get_user_model()


class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'portfolio/project_form.html'
    success_url = reverse_lazy('portfolio:project_list')

    def form_valid(self, form):
        """
        Surcharger la méthode form_valid pour ajouter des messages personnalisés ou
        des actions supplémentaires.
        """
        superuser = User.objects.filter(is_superuser=True).first()
        if not superuser:
            raise ValueError("Aucun superutilisateur n'est défini. Créez un superutilisateur avant de continuer.")

        # Associe le superutilisateur comme auteur du projet
        form.instance.created_by = superuser
        return super().form_valid(form)


class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'portfolio/project_form.html'
    success_url = reverse_lazy('portfolio:project_list')

    def form_valid(self, form):
        """
        Surcharger la méthode form_valid pour ajouter des messages personnalisés ou
        des actions supplémentaires.
        """
        return super().form_valid(form)


class ProjectDeleteView(DeleteView):
    model = Project
    template_name = 'portfolio/project_confirm_delete.html'
    success_url = reverse_lazy('portfolio:project_list')

    def delete(self, request, *args, **kwargs):
        """
        Surcharger la méthode delete pour ajouter des messages personnalisés ou
        des actions supplémentaires.
        """
        return super().delete(request, *args, **kwargs)


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
