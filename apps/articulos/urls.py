from django.urls import path
from . import views
from .views import detalle_articulo

urlpatterns = [
    path('lista/', views.lista_articulos, name='lista_articulos'),
    path('crear/', views.crear_articulo, name='crear_articulo'),
    path('detalle/<int:pk>/', views.detalle_articulo, name='detalle_articulo'), 
    path('borrar/<int:pk>/', views.borrar_articulo, name='borrar_articulo'), 
    path('editar/<int:pk>/', views.editar_articulo, name='editar_articulo'),
    path('agregar/<int:pk>/', views.agregar_comentario, name='agregar_comentario'),
    path('ver/<int:pk>/', views.ver_comentarios, name='ver_comentarios'),   
    path('editar_comentario/<int:pk>/', views.editar_comentario, name='editar_comentario'),
    path('eliminar_comentario/<int:pk>/', views.eliminar_comentario, name='eliminar_comentario'),     
]