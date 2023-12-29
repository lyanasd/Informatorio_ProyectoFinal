from django.shortcuts import render
from apps.articulos.models import Articulo

def Home(request):
    # Obtener los últimos posteos
    ultimos_posteos = Articulo.objects.order_by('-fecha_creacion')[:3]  # Obtener los últimos 4 posteos

    # Pasar los posteos al contexto
    context = {'ultimos_posteos': ultimos_posteos}

    # Renderizar la plantilla con el contexto
    return render(request, 'home.html', context)

def Post(request): 

    return render(request, 'post.html')
    