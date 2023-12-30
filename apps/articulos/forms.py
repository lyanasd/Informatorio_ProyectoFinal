from django import forms
from .models import Articulo
from .models import Comment
 
class ArticuloForm(forms.ModelForm):
    class Meta:
        model = Articulo
        fields = ['titulo', 'contenido', 'imagen', 'categoria']
        widgets = {
            'categoria': forms.Select(attrs={'class': 'form-control'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'author': forms.HiddenInput(),
            'text': forms.Textarea(attrs={'rows': 4}),
        }

class FiltroArticulosForm(forms.Form):
    CATEGORIAS_CHOICES = [
        ('', 'Todas las categorías'),  # Opción para mostrar todos los artículos sin filtrar
        ('tecnologia', 'Tecnología'),
        ('gastronomia', 'Gastronomía'),
        ('artesanias', 'Artesanías'),
        ('entretenimiento', 'Entretenimiento'),
        ('salud', 'Salud y bienestar'),
    ]
    categoria = forms.ChoiceField(choices=CATEGORIAS_CHOICES, required=False)        