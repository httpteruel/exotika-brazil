from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.forms import inlineformset_factory
from django.db import transaction
from django.db.models import Sum

from django_filters.views import FilterView

from .models import Especie, Fornecedor, CategoriaProduto, Produto, Animal, Venda, ItemVenda
from .forms import VendaForm, ItemVendaForm
from .filters import AnimalFilter, ProdutoFilter

# ==============================================================================
# CONTROLE DE ACESSO E PERMISSÕES (Requisito 3)
# ==============================================================================
class AdminRequiredMixin(UserPassesTestMixin):
    """Garante acesso apenas para superusuários ou membros do grupo 'Administradores'"""
    def test_func(self):
        return self.request.user.is_authenticated and (
            self.request.user.is_superuser or 
            self.request.user.groups.filter(name='Administradores').exists()
        )

class DonoOuAdminRequiredMixin(UserPassesTestMixin):
    """Permite acesso se o usuário for Admin/Superuser OU se for o próprio criador do registro (Requisito 3)"""
    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        if self.request.user.is_superuser or self.request.user.groups.filter(name='Administradores').exists():
            return True
        obj = self.get_object()
        return hasattr(obj, 'usuario_cadastro') and obj.usuario_cadastro == self.request.user


# ==============================================================================
# ESPECIE (Requisito 4 - Framework de Mensagens)
# ==============================================================================
class EspecieList(ListView):
    model = Especie
    template_name = 'cadastros/especie_list.html'
    context_object_name = 'especies'
    paginate_by = 10

class EspecieCreate(LoginRequiredMixin, AdminRequiredMixin, SuccessMessageMixin, CreateView):
    model = Especie
    fields = ['nome_comum', 'nome_cientifico', 'classe_biologica', 'requer_autorizacao_ibama', 'descricao', 'foto']
    template_name = 'cadastros/especie_form.html'
    success_url = reverse_lazy('listar-especie')
    success_message = "Espécie '%(nome_comum)s' cadastrada com sucesso!"

class EspecieUpdate(LoginRequiredMixin, AdminRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Especie
    fields = ['nome_comum', 'nome_cientifico', 'classe_biologica', 'requer_autorizacao_ibama', 'descricao', 'foto']
    template_name = 'cadastros/especie_form.html'
    success_url = reverse_lazy('listar-especie')
    success_message = "Espécie '%(nome_comum)s' atualizada com sucesso!"

class EspecieDelete(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Especie
    template_name = 'cadastros/especie_confirm_delete.html'
    success_url = reverse_lazy('listar-especie')

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, f"Espécie '{obj.nome_comum}' excluída com sucesso!")
        return super().delete(request, *args, **kwargs)


# ==============================================================================
# FORNECEDOR (Requisito 4 - Framework de Mensagens)
# ==============================================================================
class FornecedorList(ListView):
    model = Fornecedor
    template_name = 'cadastros/fornecedor_list.html'
    context_object_name = 'fornecedores'
    paginate_by = 10

class FornecedorCreate(LoginRequiredMixin, AdminRequiredMixin, SuccessMessageMixin, CreateView):
    model = Fornecedor
    fields = ['razao_social', 'cnpj_cpf', 'licenca_ibama', 'telefone', 'email']
    template_name = 'cadastros/fornecedor_form.html'
    success_url = reverse_lazy('listar-fornecedor')
    success_message = "Fornecedor '%(razao_social)s' cadastrado com sucesso!"

class FornecedorUpdate(LoginRequiredMixin, AdminRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Fornecedor
    fields = ['razao_social', 'cnpj_cpf', 'licenca_ibama', 'telefone', 'email']
    template_name = 'cadastros/fornecedor_form.html'
    success_url = reverse_lazy('listar-fornecedor')
    success_message = "Fornecedor '%(razao_social)s' atualizado com sucesso!"

class FornecedorDelete(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Fornecedor
    template_name = 'cadastros/fornecedor_confirm_delete.html'
    success_url = reverse_lazy('listar-fornecedor')

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, f"Fornecedor '{obj.razao_social}' excluído com sucesso!")
        return super().delete(request, *args, **kwargs)


# ==============================================================================
# CATEGORIA PRODUTO (Requisito 4 - Framework de Mensagens)
# ==============================================================================
class CategoriaProdutoList(ListView):
    model = CategoriaProduto
    template_name = 'cadastros/categoria_list.html'
    context_object_name = 'categorias'
    paginate_by = 10

class CategoriaProdutoCreate(LoginRequiredMixin, AdminRequiredMixin, SuccessMessageMixin, CreateView):
    model = CategoriaProduto
    fields = ['nome', 'descricao']
    template_name = 'cadastros/categoria_form.html'
    success_url = reverse_lazy('listar-categoria')
    success_message = "Categoria '%(nome)s' cadastrada com sucesso!"

class CategoriaProdutoUpdate(LoginRequiredMixin, AdminRequiredMixin, SuccessMessageMixin, UpdateView):
    model = CategoriaProduto
    fields = ['nome', 'descricao']
    template_name = 'cadastros/categoria_form.html'
    success_url = reverse_lazy('listar-categoria')
    success_message = "Categoria '%(nome)s' atualizada com sucesso!"

class CategoriaProdutoDelete(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = CategoriaProduto
    template_name = 'cadastros/categoria_confirm_delete.html'
    success_url = reverse_lazy('listar-categoria')

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, f"Categoria '{obj.nome}' excluída com sucesso!")
        return super().delete(request, *args, **kwargs)


# ==============================================================================
# PRODUTO (Requisito 4 - Framework de Mensagens)
# ==============================================================================
class ProdutoList(FilterView):
    model = Produto
    template_name = 'cadastros/produto_list.html'
    context_object_name = 'produtos'
    paginate_by = 10
    filterset_class = ProdutoFilter

    def get_queryset(self):
        return Produto.objects.select_related('categoria', 'fornecedor').all()

class ProdutoCreate(LoginRequiredMixin, AdminRequiredMixin, SuccessMessageMixin, CreateView):
    model = Produto
    fields = ['categoria', 'fornecedor', 'nome', 'descricao', 'preco', 'quantidade_estoque', 'imagem']
    template_name = 'cadastros/produto_form.html'
    success_url = reverse_lazy('listar-produto')
    success_message = "Produto '%(nome)s' cadastrado com sucesso!"

class ProdutoUpdate(LoginRequiredMixin, AdminRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Produto
    fields = ['categoria', 'fornecedor', 'nome', 'descricao', 'preco', 'quantidade_estoque', 'imagem']
    template_name = 'cadastros/produto_form.html'
    success_url = reverse_lazy('listar-produto')
    success_message = "Produto '%(nome)s' atualizado com sucesso!"

class ProdutoDelete(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Produto
    template_name = 'cadastros/produto_confirm_delete.html'
    success_url = reverse_lazy('listar-produto')

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, f"Produto '{obj.nome}' excluído com sucesso!")
        return super().delete(request, *args, **kwargs)


# ==============================================================================
# ANIMAL (Requisito 4 - Framework de Mensagens)
# ==============================================================================
class AnimalList(FilterView):
    model = Animal
    template_name = 'cadastros/animal_list.html'
    context_object_name = 'animais'
    paginate_by = 10
    filterset_class = AnimalFilter

    def get_queryset(self):
        qs = Animal.objects.select_related('especie', 'fornecedor', 'usuario_cadastro').all()
        if self.request.user.is_authenticated:
            if not (self.request.user.is_superuser or self.request.user.groups.filter(name='Administradores').exists()):
                qs = qs.filter(usuario_cadastro=self.request.user)
        return qs

class AnimalCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Animal
    fields = ['especie', 'fornecedor', 'microchip_anilha', 'data_nascimento', 'sexo', 'preco', 'status', 'foto']
    template_name = 'cadastros/animal_form.html'
    success_url = reverse_lazy('listar-animal')
    success_message = "Animal registrado com sucesso!"

    def form_valid(self, form):
        form.instance.usuario_cadastro = self.request.user
        return super().form_valid(form)

class AnimalUpdate(LoginRequiredMixin, DonoOuAdminRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Animal
    fields = ['especie', 'fornecedor', 'microchip_anilha', 'data_nascimento', 'sexo', 'preco', 'status', 'foto']
    template_name = 'cadastros/animal_form.html'
    success_url = reverse_lazy('listar-animal')
    success_message = "Dados do animal atualizados com sucesso!"

class AnimalDelete(LoginRequiredMixin, DonoOuAdminRequiredMixin, DeleteView):
    model = Animal
    template_name = 'cadastros/animal_confirm_delete.html'
    success_url = reverse_lazy('listar-animal')

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, f"Registro do animal '{obj.microchip_anilha}' excluído com sucesso!")
        return super().delete(request, *args, **kwargs)


# ==============================================================================
# VENDA (Requisito 4 - Framework de Mensagens)
# ==============================================================================
ItemVendaFormSet = inlineformset_factory(
    Venda, ItemVenda, form=ItemVendaForm, extra=1, can_delete=True
)

class VendaList(LoginRequiredMixin, ListView):
    model = Venda
    template_name = 'cadastros/venda_list.html'
    context_object_name = 'vendas'
    paginate_by = 10

    def get_queryset(self):
        qs = Venda.objects.select_related('cliente').prefetch_related('itens__produto', 'itens__animal')
        if self.request.user.is_superuser or self.request.user.groups.filter(name='Administradores').exists():
            return qs.all()
        return qs.filter(cliente=self.request.user)


class VendaCreate(LoginRequiredMixin, CreateView):
    model = Venda
    form_class = VendaForm
    template_name = 'cadastros/venda_form.html'
    success_url = reverse_lazy('listar-venda')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['itens'] = ItemVendaFormSet(self.request.POST)
        else:
            data['itens'] = ItemVendaFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        itens = context['itens']
        form.instance.cliente = self.request.user

        with transaction.atomic():
            self.object = form.save()
            if itens.is_valid():
                itens.instance = self.object
                itens_salvos = itens.save()

                valor_total = 0
                for item in itens_salvos:
                    valor_total += item.quantidade * item.preco_unitario

                    if item.produto:
                        item.produto.quantidade_estoque -= item.quantidade
                        item.produto.save()

                    if item.animal:
                        item.animal.status = 'VENDIDO'
                        item.animal.save()

                self.object.valor_total = valor_total
                self.object.status = 'CONCLUIDA'
                self.object.save()
                messages.success(self.request, f"Venda nº #{self.object.id} concluída com sucesso!")

        return super().form_valid(form)


# ==============================================================================
# DETALHES VENDA
# ==============================================================================
class VendaDetail(LoginRequiredMixin, DetailView):
    model = Venda
    template_name = 'cadastros/venda_detail.html'
    context_object_name = 'venda'

    def get_queryset(self):
        qs = Venda.objects.select_related('cliente').prefetch_related('itens__produto', 'itens__animal')
        if self.request.user.is_superuser or self.request.user.groups.filter(name='Administradores').exists():
            return qs.all()
        return qs.filter(cliente=self.request.user)


# ==============================================================================
# DASHBOARD 
# ==============================================================================
class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_especies'] = Especie.objects.count()
        context['total_animais'] = Animal.objects.count()
        context['animais_disponiveis'] = Animal.objects.filter(status='DISPONIVEL').count()
        context['total_produtos'] = Produto.objects.count()
        context['total_vendas'] = Venda.objects.filter(status='CONCLUIDA').count()
        
        faturamento = Venda.objects.filter(status='CONCLUIDA').aggregate(Sum('valor_total'))['valor_total__sum']
        context['total_faturamento'] = faturamento or 0.00
        return context