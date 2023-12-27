from django.db import models
from django.contrib.auth.models import User

class Articulo(models.Model):
    titulo = models.CharField(max_length=255)
    contenido = models.TextField()
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

def detalle_articulo(request, pk):
    # Recupera el artículo usando el identificador único (pk)
    articulo = get_object_or_404(Articulo, pk=pk)

    # Pasar el artículo al template
    return render(request, 'articulos/detalle_articulo.html', {'articulo': articulo})        