from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from .models import Articulo
from .forms import ArticuloForm

def detalle_articulo(request, pk):
    articulo = get_object_or_404(Articulo, pk=pk)
    return render(request, 'articulos/detalle_articulo.html', {'articulo': articulo})

def lista_articulos(request):
    # Obtén todos los artículos
    lista_articulos = Articulo.objects.all()

    # Configura la paginación
    paginator = Paginator(lista_articulos, 8) 
    page = request.GET.get('page')

    try:
        articulos = paginator.page(page)
    except PageNotAnInteger:
        # Si la página no es un entero, entrega la primera página
        articulos = paginator.page(1)
    except EmptyPage:
        # Si la página está fuera de rango, entrega la última página
        articulos = paginator.page(paginator.num_pages)

    context = {'articulos': articulos}
    return render(request, 'articulos/lista_articulos.html', context)
 
def crear_articulo(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ArticuloForm(request.POST, request.FILES)
            if form.is_valid():
                nuevo_articulo = form.save(commit=False)
                nuevo_articulo.autor = request.user
                nuevo_articulo.save()
                return redirect(reverse('articulos:lista_articulos'))  # Asegúrate de usar el nombre correcto
        else:
            form = ArticuloForm()
        return render(request, 'articulos/crear_articulo.html', {'form': form})
    else:
        # Redirigir al usuario no autenticado a la página de inicio de sesión
        return redirect('login')