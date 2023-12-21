from django.shortcuts import render, redirect
from .models import Articulo
from .forms import ArticuloForm

def lista_articulos(request):
    articulos = Articulo.objects.all()
    return render(request, 'articulos/lista_articulos.html', {'articulos': articulos})
 
def crear_articulo(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ArticuloForm(request.POST, request.FILES)
            if form.is_valid():
                nuevo_articulo = form.save(commit=False)
                nuevo_articulo.autor = request.user
                nuevo_articulo.save()
                return redirect('lista_articulos')
        else:
            form = ArticuloForm()
        return render(request, 'articulos/crear_articulo.html', {'form': form})
    else:
        # Redirigir al usuario no autenticado a la página de inicio de sesión
        return redirect('login')