from django.urls import path
from .views import VendaList, VendaCreate
from .views import (
    EspecieList, EspecieCreate, EspecieUpdate, EspecieDelete,
    FornecedorList, FornecedorCreate, FornecedorUpdate, FornecedorDelete,
    CategoriaProdutoList, CategoriaProdutoCreate, CategoriaProdutoUpdate, CategoriaProdutoDelete,
    ProdutoList, ProdutoCreate, ProdutoUpdate, ProdutoDelete,
    AnimalList, AnimalCreate, AnimalUpdate, AnimalDelete
)

urlpatterns = [
    # Espécies
    path('especies/', EspecieList.as_view(), name='listar-especie'),
    path('especies/cadastrar/', EspecieCreate.as_view(), name='cadastrar-especie'),
    path('especies/editar/<int:pk>/', EspecieUpdate.as_view(), name='editar-especie'),
    path('especies/excluir/<int:pk>/', EspecieDelete.as_view(), name='excluir-especie'),

    # Fornecedores
    path('fornecedores/', FornecedorList.as_view(), name='listar-fornecedor'),
    path('fornecedores/cadastrar/', FornecedorCreate.as_view(), name='cadastrar-fornecedor'),
    path('fornecedores/editar/<int:pk>/', FornecedorUpdate.as_view(), name='editar-fornecedor'),
    path('fornecedores/excluir/<int:pk>/', FornecedorDelete.as_view(), name='excluir-fornecedor'),

    # Categorias de Produtos
    path('categorias/', CategoriaProdutoList.as_view(), name='listar-categoria'),
    path('categorias/cadastrar/', CategoriaProdutoCreate.as_view(), name='cadastrar-categoria'),
    path('categorias/editar/<int:pk>/', CategoriaProdutoUpdate.as_view(), name='editar-categoria'),
    path('categorias/excluir/<int:pk>/', CategoriaProdutoDelete.as_view(), name='excluir-categoria'),

    # Produtos
    path('produtos/', ProdutoList.as_view(), name='listar-produto'),
    path('produtos/cadastrar/', ProdutoCreate.as_view(), name='cadastrar-produto'),
    path('produtos/editar/<int:pk>/', ProdutoUpdate.as_view(), name='editar-produto'),
    path('produtos/excluir/<int:pk>/', ProdutoDelete.as_view(), name='excluir-produto'),

    # Animais
    path('animais/', AnimalList.as_view(), name='listar-animal'),
    path('animais/cadastrar/', AnimalCreate.as_view(), name='cadastrar-animal'),
    path('animais/editar/<int:pk>/', AnimalUpdate.as_view(), name='editar-animal'),
    path('animais/excluir/<int:pk>/', AnimalDelete.as_view(), name='excluir-animal'),

    # Vendas
    path('vendas/', VendaList.as_view(), name='listar-venda'),
    path('vendas/cadastrar/', VendaCreate.as_view(), name='cadastrar-venda'),
]