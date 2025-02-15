from django import forms
from .models import Project
from ckeditor.widgets import CKEditorWidget


class ProjectForm(forms.ModelForm):
    """
    Formulaire pour gérer les champs liés au modèle Project.
    """
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Project
        fields = ['title', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez le titre du projet'
            }),
            # 'description': forms.Textarea(attrs={
            #     'class': 'form-control',
            #     'placeholder': 'Entrez une description détaillée du projet',
            #     'rows': 5
            # }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
        }
        labels = {
            'title': 'Titre du projet',
            'description': 'Description',
            'image': 'Image de garde',
        }
        help_texts = {
            'image': 'Téléchargez une image de garde pour le projet (formats acceptés : JPEG, PNG).',
        }

    def clean_title(self):
        """
        Validation personnalisée pour le champ 'title'.
        """
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError(
                "Le titre doit contenir au moins 5 caractères."
            )
        return title
