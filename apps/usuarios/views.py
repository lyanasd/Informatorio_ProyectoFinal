from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views import View
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import RegistroForm

class Registro(CreateView):
    form_class = RegistroForm
    success_url = reverse_lazy('login')
    template_name = 'usuarios/registro.html'

class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect('home')
