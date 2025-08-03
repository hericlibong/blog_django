from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget

from .models import Post


class PostForm(forms.ModelForm):
    """
    Form for creating and updating blog posts.
    """

    content = forms.CharField(widget=CKEditor5Widget(config_name='default'))

    class Meta:
        model = Post
        fields = [
            'title',
            'subtitle',
            'image',
            'content',
            'category',
            'tags',
            'is_published',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'subtitle': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'category': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'title': 'Titre',
            'subtitle': 'Sous-titre',
            'image': 'Image de couverture',
            'content': "Contenu de l'article",
            'category': 'Categories',
            'tags': 'Tags',
            'is_published': 'Publié',
        }
