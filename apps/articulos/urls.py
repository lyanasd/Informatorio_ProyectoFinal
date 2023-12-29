from django.urls import path
from . import views

urlpatterns = [
    path('lista/', views.lista_articulos, name='lista_articulos'),
    path('crear/', views.crear_articulo, name='crear_articulo'),
    path('detalle/<int:pk>/', views.detalle_articulo, name='detalle_articulo'), 
    path('borrar/<int:pk>/', views.borrar_articulo, name='borrar_articulo'), 
    path('editar/<int:pk>/', views.editar_articulo, name='editar_articulo'),
]