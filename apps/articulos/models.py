from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Articulo(models.Model):
    CATEGORIAS_CHOICES = [
        ('tecnologia', 'Tecnología'),
        ('gastronomia', 'Gastronomía'),
        ('artesanias', 'Artesanías'),
        ('entretenimiento', 'Entretenimiento'),
        ('salud', 'Salud y bienestar'),
    ]

    categoria = models.CharField(max_length=20, choices=CATEGORIAS_CHOICES, blank=True, null=True)
    titulo = models.CharField(max_length=255)
    contenido = models.TextField()
    imagen = models.ImageField(upload_to='articulos_imagenes/', blank=True, null=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return self.titulo

class Comment(models.Model):
    articulo = models.ForeignKey('Articulo', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text 