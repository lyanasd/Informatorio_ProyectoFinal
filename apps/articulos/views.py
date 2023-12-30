from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Articulo
from .forms import ArticuloForm, CommentForm, FiltroArticulosForm
from django.shortcuts import render, get_object_or_404
from .models import Comment

def editar_comentario(request, pk):
    comentario = get_object_or_404(Comment, pk=pk)
    if request.user == comentario.author:
        if request.method == 'POST':
            form = CommentForm(request.POST, instance=comentario)
            if form.is_valid():
                form.save()
                return redirect('articulos:detalle_articulo', pk=comentario.articulo.pk)
        else:
            form = CommentForm(instance=comentario)
        return render(request, 'articulos/editar_comentario.html', {'form': form})
    else:
        # Manejar el caso donde el usuario no es el autor del comentario
        return redirect('articulos:detalle_articulo', pk=comentario.articulo.pk)

def eliminar_comentario(request, pk):
    comentario = get_object_or_404(Comment, pk=pk)
    
    if request.user == comentario.author:
        if request.method == 'POST':
            # Eliminar el comentario y redirigir al detalle del artículo
            articulo_pk = comentario.articulo.pk
            comentario.delete()
            return redirect('articulos:detalle_articulo', pk=articulo_pk)
        else:
            # Asegúrate de incluir el objeto articulo en el contexto
            return render(request, 'articulos/borrar_comentario.html', {'comentario': comentario, 'articulo': comentario.articulo})
    else:
        # Redirigir al detalle del artículo si el usuario no tiene permisos
        return redirect('articulos:detalle_articulo', pk=comentario.articulo.pk)

def agregar_comentario(request, pk):
    if request.method == 'POST':
        comentario_texto = request.POST.get('comentario_texto')
        Comment.objects.create(articulo_id=pk, author=request.user, text=comentario_texto)
    return redirect('articulos:detalle_articulo', pk=pk)

def ver_comentarios(request, pk):
    articulo_comentarios = Comment.objects.filter(articulo_id=pk)
    return render(request, 'articulos/detalle_articulo.html', {'comentarios': articulo_comentarios})

@login_required(login_url='/login/')
def editar_articulo(request, pk):
    articulo = get_object_or_404(Articulo, pk=pk)

    # Verificar si el usuario actual es el autor del artículo
    if request.user == articulo.autor:
 
        if request.method == 'POST':
            form = ArticuloForm(request.POST, request.FILES, instance=articulo)
            if form.is_valid():
                form.save()
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
    comentarios = Comment.objects.filter(articulo=articulo)
    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.articulo = articulo
            comentario.author = request.user
            comentario.save()
            return redirect('articulos:detalle_articulo', pk=pk)

    return render(request, 'articulos/detalle_articulo.html', {'articulo': articulo, 'comentarios': comentarios, 'form': form})

def lista_articulos(request):
    # Obtener todos los artículos
    articulos = Articulo.objects.all()
    articulos = articulos.order_by('-fecha_creacion')

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

    # Paginación
    paginator = Paginator(articulos, 8)
    page = request.GET.get('page')

    try:
        articulos = paginator.page(page)
    except PageNotAnInteger:
        articulos = paginator.page(1)
    except EmptyPage:
        articulos = paginator.page(paginator.num_pages)

    # Crea una instancia del formulario de filtrado y pásalo al contexto
    filtro_form = FiltroArticulosForm(request.GET)
    categorias_choices = Articulo.CATEGORIAS_CHOICES

    context = {'articulos': articulos, 'categorias_choices': categorias_choices, 'filtro_form': filtro_form}
    return render(request, 'articulos/lista_articulos.html', context)
 
@login_required(login_url='/login/') # Requerir la autenticación del usuario
def crear_articulo(request):

    if request.method == 'POST':

        form = ArticuloForm(request.POST, request.FILES)
        
        if form.is_valid():
            articulo = form.save(commit=False)
            
            # Asignar el autor del artículo como el usuario actual
            articulo.autor = request.user
            
            articulo.save()
            
            # Redirigir a la página de detalle del artículo recién creado
            return redirect('articulos:detalle_articulo', pk=articulo.id)
    else:
        # Si la solicitud no es de tipo POST, crear una instancia vacía del formulario
        form = ArticuloForm()
        
    return render(request, 'articulos/crear_articulo.html', {'form': form})

def detalle_articulo(request, pk):
    articulo = get_object_or_404(Articulo, pk=pk)
    comentarios = Comment.objects.filter(articulo=articulo)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.articulo = articulo
            comentario.author = request.user
            comentario.save()

    else:
        form = CommentForm()

    return render(request, 'articulos/detalle_articulo.html', {'articulo': articulo, 'comentarios': comentarios, 'form': form})