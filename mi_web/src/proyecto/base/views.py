from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
#from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Tarea

# Create your views here.

class logueo(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('pendientes')


class PaginaRegistro(FormView):
    template_name = 'base/registro.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('pendientes')

    def form_valid(self, form):
        usuario = form.save(commit=True)
        if usuario is not None:
            login(self.request, usuario)
        return super(PaginaRegistro, self).form_valid(form)


class ListaPendientes(LoginRequiredMixin,ListView):
    #models = Tarea 
    queryset = Tarea.objects.all() # conjunto de datos personalizado, define el queryset directamente en la vista
    context_object_name = "tareas"

    
    def get_context_data(self, **kwargs):
        # Primero, obtén el contexto base del método padre
        context = super().get_context_data(**kwargs)
        
        # Agrega más datos al contexto si es necesario
        context['tareas'] = context['tareas'].filter(usuario=self.request.user)
        context['count'] = context['tareas'].filter(completo=False).count()

        valor_buscado = self.request.GET.get('area-buscar') or ''
        if valor_buscado:
            context['tareas'] = context['tareas'].filter(titulo__icontains=valor_buscado)
        context["valor_buscado"] = valor_buscado

        # Retorna el contexto actualizado
        return context


class DetalleTarea(LoginRequiredMixin,DetailView):
    model = Tarea
    context_object_name = "tarea"
    template_name = 'base/tarea.html'


class CrearTarea(LoginRequiredMixin,CreateView):
    model= Tarea
    fields = ['titulo','descripcion','completo']
    success_url = reverse_lazy('pendientes')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super (CrearTarea, self).form_valid(form)

class EditarTarea(LoginRequiredMixin,UpdateView):
    model= Tarea
    fields = ['titulo','descripcion','completo'] # '__all__' para mostrar todos los campos 
    success_url = reverse_lazy('pendientes')


class EliminarTarea(LoginRequiredMixin,DeleteView):
    model = Tarea
    context_objecto_name = "tareas"
    success_url = reverse_lazy('pendientes')
    template_name = 'base/tarea_confirm_delete.html'

