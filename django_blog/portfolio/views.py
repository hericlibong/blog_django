from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from accounts.models import UserProfile

from .forms import ProjectForm
from .models import Project

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
    ordering = ['-created_at']
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["profile"] = UserProfile.objects.first()
        return context


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'portfolio/project_detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = UserProfile.objects.first()
        return context


class AboutView(TemplateView):
    template_name = 'portfolio/about.html'
