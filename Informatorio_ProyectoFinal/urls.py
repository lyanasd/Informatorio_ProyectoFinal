from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.Home, name ='inicio'),
    path('contacto', views.Contacto, name = 'contacto'),
    path('post', views.Post, name = 'post'),

    #APP USUARIOs
    path('usuarios/', include('apps.usuarios.urls')),

    #LOGIN Y LOGOUT
    path('login/',auth.LoginView.as_view(template_name='usuarios/login.html'), name ='login'),
    path('logout/',auth.LogoutView.as_view(), name ='logout'),

    #APP ARTICULOS
    #path('articulos/', include('apps.articulos.urls')),
    path('articulos/', include(('apps.articulos.urls', 'articulos'))),

]

urlpatterns+=staticfiles_urlpatterns()
