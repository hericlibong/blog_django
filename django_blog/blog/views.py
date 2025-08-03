from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
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

from .forms import PostForm
from .models import Category, Post


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user == obj.author or self.request.user.is_superuser:
            return obj
        raise Http404("Vous n'avez pas la permission de supprimer cet article.")


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        user = self.request.user
        if post.is_published or user == post.author or user.is_superuser:
            return post
        raise Http404("Cet article n'est pas disponible.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = UserProfile.objects.first()
        context['categories'] = Category.objects.all()  # utile pour navigation
        return context


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:post_create_success')  # redirection temporaire
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user == obj.author or self.request.user.is_superuser:
            return obj
        raise Http404("Vous n'avez pas la permission de modifier cet article.")

    def get_success_url(self):
        return reverse_lazy('blog:post_create_success') + f'?action=update&id={self.object.id}'

    def form_valid(self, form):
        action = self.request.POST.get("action")
        if action == "publish":
            form.instance.is_published = True
        else:
            form.instance.is_published = False
        return super().form_valid(form)


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        queryset = Post.objects.all()

        # Filtrage des articles selon le statut de l'utilisateur
        if user.is_authenticated and user.is_staff:
            queryset = queryset.filter(author=user)
        else:
            queryset = queryset.filter(is_published=True)

        # Filtrage par catégorie si catégorie sélectionnée
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        # Filtrage par tag si tag sélectionné
        tag_slug = self.request.GET.get('tag')
        if tag_slug:
            queryset = queryset.filter(tags__name__iexact=tag_slug)

        # Filtrage par type de publication (brouillon ou publié)
        filter_type = self.request.GET.get('filter')
        if filter_type == 'draft':
            queryset = queryset.filter(is_published=False)
        elif filter_type == 'published':
            queryset = queryset.filter(is_published=True)

        return queryset.order_by('-created_at')

    # 👇 Ici, tu ajoutes le contexte "profile"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  # Récupérer toutes les catégories

        # Afficher le profil de l'administrateur
        context['profile'] = UserProfile.objects.first()
        category_slug = self.request.GET.get('category')
        if category_slug:
            category = Category.objects.filter(slug=category_slug).first()
            context['selected_category'] = category
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:post_create_success')

    def form_valid(self, form):
        form.instance.author = self.request.user
        action = self.request.POST.get('action')

        if action == 'publish':
            form.instance.is_published = True
        else:
            form.instance.is_published = False

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:post_create_success') + f'?action=create&id={self.object.id}'


class PostCreateSuccessView(TemplateView):
    template_name = 'blog/post_create_success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_id = self.request.GET.get('id')
        try:
            post = Post.objects.get(id=post_id, author=self.request.user)
            context['post_published'] = post.is_published
            context['action'] = self.request.GET.get('action', 'create')
        except Post.DoesNotExist:
            context['post_published'] = False
            context['action'] = 'create'
        return context


# class BeautifulF1ListView(ListView):
#     model = Post
#     template_name = 'blog/beautifull_f1.html'
#     context_object_name = 'posts'
#     ordering = ['-created_at']
#     paginate_by = 10

#     def get_queryset(self):
#         return Post.objects.filter(
#             is_published=True,
#             categories__name__iexact="Beautifull F1"
#         )
