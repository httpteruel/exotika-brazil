from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Especie

class EspecieList(ListView):
    model = Especie
    template_name = 'cadastros/especie_list.html'
    context_object_name = 'especies'
    paginate_by = 10


class EspecieCreate(LoginRequiredMixin, CreateView):
    model = Especie
    fields = ['nome_comum', 'nome_cientifico', 'classe_biologica', 'requer_autorizacao_ibama', 'descricao', 'foto']
    template_name = 'cadastros/especie_form.html'
    success_url = reverse_lazy('listar-especie')


class EspecieUpdate(LoginRequiredMixin, UpdateView):
    model = Especie
    fields = ['nome_comum', 'nome_cientifico', 'classe_biologica', 'requer_autorizacao_ibama', 'descricao', 'foto']
    template_name = 'cadastros/especie_form.html'
    success_url = reverse_lazy('listar-especie')


class EspecieDelete(LoginRequiredMixin, DeleteView):
    model = Especie
    template_name = 'cadastros/especie_confirm_delete.html'
    success_url = reverse_lazy('listar-especie')