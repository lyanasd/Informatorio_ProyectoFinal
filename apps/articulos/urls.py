from django.urls import path
from . import views

urlpatterns = [
    path('lista/', views.lista_articulos, name='lista_articulos'),
    path('crear/', views.crear_articulo, name='crear_articulo'),
    path('detalle/<int:pk>/', views.detalle_articulo, name='detalle_articulo'),
    
]