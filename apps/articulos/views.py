from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Articulo
from .forms import ArticuloForm
from django.contrib import messages # ?

@login_required(login_url='/login/')
def editar_articulo(request, pk):
    articulo = get_object_or_404(Articulo, pk=pk)

    # Verificar si el usuario actual es el autor del artículo
    if request.user == articulo.autor:
 
        if request.method == 'POST':
            form = ArticuloForm(request.POST, request.FILES, instance=articulo)
            if form.is_valid():
                form.save()
                messages.success(request, 'Artículo editado con éxito.')
                return redirect('articulos:detalle_articulo', pk=articulo.id)
        else:
            form = ArticuloForm(instance=articulo)

    return render(request, 'articulos/editar_articulo.html', {'form': form, 'articulo': articulo})

@login_required(login_url='/login/')  
def borrar_articulo(request, pk):
    articulo = get_object_or_404(Articulo, pk=pk)

    # Verificar si el usuario actual es el autor del artículo
    if request.user == articulo.autor:

        if request.method == 'POST':
            articulo.delete()
            return redirect('articulos:lista_articulos')

        return render(request, 'articulos/borrar_articulo.html', {'articulo': articulo})

    # Si el usuario no es el autor redirigirlo a la página de detalle del artículo.
    return redirect('articulos:detalle_articulo', pk=pk)

def detalle_articulo(request, pk):
    articulo = get_object_or_404(Articulo, pk=pk)

    # Verificar si el campo 'imagen' tiene un valor antes de renderizar la plantilla
    if articulo.imagen:
        return render(request, 'articulos/detalle_articulo.html', {'articulo': articulo})
    else:
        return render(request, 'articulos/detalle_articulo.html', {'articulo': articulo, 'imagen_vacia': True})

def lista_articulos(request):
    # Obtén todos los artículos
    articulos = Articulo.objects.all()

    # Filtrado por categoría
    categoria = request.GET.get('categoria')
    if categoria:
        articulos = articulos.filter(categoria=categoria)

    # Filtrado por antigüedad
    antiguedad = request.GET.get('antiguedad')
    if antiguedad == 'asc':
        articulos = articulos.order_by('fecha_creacion')
    elif antiguedad == 'desc':
        articulos = articulos.order_by('-fecha_creacion')

    # Filtrado por orden alfabético
    orden = request.GET.get('orden')
    if orden == 'asc':
        articulos = articulos.order_by('titulo')
    elif orden == 'desc':
        articulos = articulos.order_by('-titulo')

    # Configura la paginación
    paginator = Paginator(articulos, 8)
    page = request.GET.get('page')

    try:
        articulos = paginator.page(page)
    except PageNotAnInteger:
        articulos = paginator.page(1)
    except EmptyPage:
        articulos = paginator.page(paginator.num_pages)

    context = {'articulos': articulos}
    return render(request, 'articulos/lista_articulos.html', context)
 
@login_required(login_url='/login/') # Requerir la autenticación del usuario
def crear_articulo(request):
    # Verificar si la solicitud es de tipo POST 
    if request.method == 'POST':
        # Crear una instancia del formulario ArticuloForm con los datos de la solicitud
        form = ArticuloForm(request.POST, request.FILES)
        
        # Verificar si el formulario es válido
        if form.is_valid():
            # Guardar el artículo en la base de datos sin confirmar la operación
            articulo = form.save(commit=False)
            
            # Asignar el autor del artículo como el usuario actual
            articulo.autor = request.user
            
            # Confirmar la operación de guardado en la base de datos
            articulo.save()
            
            # Redirigir a la página de detalle del artículo recién creado
            return redirect('articulos:detalle_articulo', pk=articulo.id)
    else:
        # Si la solicitud no es de tipo POST, crear una instancia vacía del formulario
        form = ArticuloForm()
        
    return render(request, 'articulos/crear_articulo.html', {'form': form})
