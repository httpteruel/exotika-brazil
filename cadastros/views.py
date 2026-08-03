from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.forms import inlineformset_factory
from django.db import transaction
from django.db.models import Sum

from .models import Especie, Fornecedor, CategoriaProduto, Produto, Animal, Venda, ItemVenda
from .forms import VendaForm, ItemVendaForm


# ==============================================================================
# MIXIN DE PROTEÇÃO POR GRUPO / PERMISSÃO (2º TRIMESTRE)
# ==============================================================================
class AdminRequiredMixin(UserPassesTestMixin):
    """Garante acesso apenas para superusuários ou membros do grupo 'Administradores'"""
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(name='Administradores').exists()


# ==============================================================================
# 1. ESPÉCIE
# ==============================================================================
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

class EspecieDelete(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Especie
    template_name = 'cadastros/especie_confirm_delete.html'
    success_url = reverse_lazy('listar-especie')


# ==============================================================================
# 2. FORNECEDOR
# ==============================================================================
class FornecedorList(ListView):
    model = Fornecedor
    template_name = 'cadastros/fornecedor_list.html'
    context_object_name = 'fornecedores'
    paginate_by = 10

class FornecedorCreate(LoginRequiredMixin, CreateView):
    model = Fornecedor
    fields = ['razao_social', 'cnpj_cpf', 'licenca_ibama', 'telefone', 'email']
    template_name = 'cadastros/fornecedor_form.html'
    success_url = reverse_lazy('listar-fornecedor')

class FornecedorUpdate(LoginRequiredMixin, UpdateView):
    model = Fornecedor
    fields = ['razao_social', 'cnpj_cpf', 'licenca_ibama', 'telefone', 'email']
    template_name = 'cadastros/fornecedor_form.html'
    success_url = reverse_lazy('listar-fornecedor')

class FornecedorDelete(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Fornecedor
    template_name = 'cadastros/fornecedor_confirm_delete.html'
    success_url = reverse_lazy('listar-fornecedor')


# ==============================================================================
# 3. CATEGORIA DE PRODUTO
# ==============================================================================
class CategoriaProdutoList(ListView):
    model = CategoriaProduto
    template_name = 'cadastros/categoria_list.html'
    context_object_name = 'categorias'
    paginate_by = 10

class CategoriaProdutoCreate(LoginRequiredMixin, CreateView):
    model = CategoriaProduto
    fields = ['nome', 'descricao']
    template_name = 'cadastros/categoria_form.html'
    success_url = reverse_lazy('listar-categoria')

class CategoriaProdutoUpdate(LoginRequiredMixin, UpdateView):
    model = CategoriaProduto
    fields = ['nome', 'descricao']
    template_name = 'cadastros/categoria_form.html'
    success_url = reverse_lazy('listar-categoria')

class CategoriaProdutoDelete(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = CategoriaProduto
    template_name = 'cadastros/categoria_confirm_delete.html'
    success_url = reverse_lazy('listar-categoria')


# ==============================================================================
# 4. PRODUTO
# ==============================================================================
class ProdutoList(ListView):
    model = Produto
    template_name = 'cadastros/produto_list.html'
    context_object_name = 'produtos'
    paginate_by = 10
    queryset = Produto.objects.select_related('categoria', 'fornecedor').all()

class ProdutoCreate(LoginRequiredMixin, CreateView):
    model = Produto
    fields = ['categoria', 'fornecedor', 'nome', 'descricao', 'preco', 'quantidade_estoque', 'imagem']
    template_name = 'cadastros/produto_form.html'
    success_url = reverse_lazy('listar-produto')

class ProdutoUpdate(LoginRequiredMixin, UpdateView):
    model = Produto
    fields = ['categoria', 'fornecedor', 'nome', 'descricao', 'preco', 'quantidade_estoque', 'imagem']
    template_name = 'cadastros/produto_form.html'
    success_url = reverse_lazy('listar-produto')

class ProdutoDelete(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Produto
    template_name = 'cadastros/produto_confirm_delete.html'
    success_url = reverse_lazy('listar-produto')


# ==============================================================================
# 5. ANIMAL
# ==============================================================================
class AnimalList(ListView):
    model = Animal
    template_name = 'cadastros/animal_list.html'
    context_object_name = 'animais'
    paginate_by = 10
    queryset = Animal.objects.select_related('especie', 'fornecedor').all()

class AnimalCreate(LoginRequiredMixin, CreateView):
    model = Animal
    fields = ['especie', 'fornecedor', 'microchip_anilha', 'data_nascimento', 'sexo', 'preco', 'status', 'foto']
    template_name = 'cadastros/animal_form.html'
    success_url = reverse_lazy('listar-animal')

class AnimalUpdate(LoginRequiredMixin, UpdateView):
    model = Animal
    fields = ['especie', 'fornecedor', 'microchip_anilha', 'data_nascimento', 'sexo', 'preco', 'status', 'foto']
    template_name = 'cadastros/animal_form.html'
    success_url = reverse_lazy('listar-animal')

class AnimalDelete(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Animal
    template_name = 'cadastros/animal_confirm_delete.html'
    success_url = reverse_lazy('listar-animal')


# ==============================================================================
# 6. VENDA
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
        # Admins e Superusuários podem ver todas as vendas; usuários comuns veem APENAS as suas
        if self.request.user.is_superuser or self.request.user.groups.filter(name='Administradores').exists():
            return Venda.objects.select_related('cliente').all()
        return Venda.objects.filter(cliente=self.request.user).select_related('cliente')


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

        # Atribui o usuário logado como o cliente da venda automaticamente
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

        return super().form_valid(form)


# ==============================================================================
# 7. DETALHES DA VENDA (DetailView)
# ==============================================================================
class VendaDetail(LoginRequiredMixin, DetailView):
    model = Venda
    template_name = 'cadastros/venda_detail.html'
    context_object_name = 'venda'

    def get_queryset(self):
        # Impede que um usuário veja os detalhes de uma venda que não é dele (a não ser que seja admin)
        if self.request.user.is_superuser or self.request.user.groups.filter(name='Administradores').exists():
            return Venda.objects.all()
        return Venda.objects.filter(cliente=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['itens'] = ItemVenda.objects.filter(venda=self.object).select_related('produto', 'animal')
        return context


# ==============================================================================
# 8. PAGINA INICIAL / DASHBOARD
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