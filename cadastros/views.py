from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.db import transaction

from .models import Especie, Fornecedor, CategoriaProduto, Produto, Animal, Venda, ItemVenda
from .forms import VendaForm, ItemVendaForm


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

class EspecieDelete(LoginRequiredMixin, DeleteView):
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

class FornecedorDelete(LoginRequiredMixin, DeleteView):
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

class CategoriaProdutoDelete(LoginRequiredMixin, DeleteView):
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

class ProdutoDelete(LoginRequiredMixin, DeleteView):
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

class AnimalDelete(LoginRequiredMixin, DeleteView):
    model = Animal
    template_name = 'cadastros/animal_confirm_delete.html'
    success_url = reverse_lazy('listar-animal')


# ==============================================================================
# 6. VENDA
# ==============================================================================
ItemVendaFormSet = inlineformset_factory(
    Venda, ItemVenda, form=ItemVendaForm, extra=1, can_delete=True
)

class VendaList(ListView):
    model = Venda
    template_name = 'cadastros/venda_list.html'
    context_object_name = 'vendas'
    paginate_by = 10

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
        with transaction.atomic():
            self.object = form.save()
            if itens.is_valid():
                itens.instance = self.object
                itens_salvos = itens.save()

                valor_total = 0
                for item in itens_salvos:
                    valor_total += item.quantidade * item.preco_unitario

                    # Regra de negócio 1: Baixa no estoque do Produto
                    if item.produto:
                        item.produto.quantidade_estoque -= item.quantidade
                        item.produto.save()

                    # Regra de negócio 2: Atualização do status do Animal
                    if item.animal:
                        item.animal.status = 'VENDIDO'
                        item.animal.save()

                self.object.valor_total = valor_total
                self.object.status = 'CONCLUIDA'
                self.object.save()

        return super().form_valid(form)