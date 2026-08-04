from django.urls import path
from .views import (
    EspecieList, EspecieCreate, EspecieUpdate, EspecieDelete,
    FornecedorList, FornecedorCreate, FornecedorUpdate, FornecedorDelete,
    CategoriaProdutoList, CategoriaProdutoCreate, CategoriaProdutoUpdate, CategoriaProdutoDelete,
    ProdutoList, ProdutoCreate, ProdutoUpdate, ProdutoDelete,
    AnimalList, AnimalCreate, AnimalUpdate, AnimalDelete,
    VendaList, VendaCreate, VendaDetail
)

urlpatterns = [
    # Espécie
    path('listar/especies/', EspecieList.as_view(), name='listar-especie'),
    path('cadastrar/especie/', EspecieCreate.as_view(), name='cadastrar-especie'),
    path('editar/especie/<int:pk>/', EspecieUpdate.as_view(), name='editar-especie'),
    path('deletar/especie/<int:pk>/', EspecieDelete.as_view(), name='deletar-especie'),
    path('excluir/especie/<int:pk>/', EspecieDelete.as_view(), name='excluir-especie'),

    # Fornecedor
    path('listar/fornecedores/', FornecedorList.as_view(), name='listar-fornecedor'),
    path('cadastrar/fornecedor/', FornecedorCreate.as_view(), name='cadastrar-fornecedor'),
    path('editar/fornecedor/<int:pk>/', FornecedorUpdate.as_view(), name='editar-fornecedor'),
    path('deletar/fornecedor/<int:pk>/', FornecedorDelete.as_view(), name='deletar-fornecedor'),
    path('excluir/fornecedor/<int:pk>/', FornecedorDelete.as_view(), name='excluir-fornecedor'),

    # Categoria
    path('listar/categorias/', CategoriaProdutoList.as_view(), name='listar-categoria'),
    path('cadastrar/categoria/', CategoriaProdutoCreate.as_view(), name='cadastrar-categoria'),
    path('editar/categoria/<int:pk>/', CategoriaProdutoUpdate.as_view(), name='editar-categoria'),
    path('deletar/categoria/<int:pk>/', CategoriaProdutoDelete.as_view(), name='deletar-categoria'),
    path('excluir/categoria/<int:pk>/', CategoriaProdutoDelete.as_view(), name='excluir-categoria'),

    # Produto
    path('listar/produtos/', ProdutoList.as_view(), name='listar-produto'),
    path('cadastrar/produto/', ProdutoCreate.as_view(), name='cadastrar-produto'),
    path('editar/produto/<int:pk>/', ProdutoUpdate.as_view(), name='editar-produto'),
    path('deletar/produto/<int:pk>/', ProdutoDelete.as_view(), name='deletar-produto'),
    path('excluir/produto/<int:pk>/', ProdutoDelete.as_view(), name='excluir-produto'),

    # Animal
    path('listar/animais/', AnimalList.as_view(), name='listar-animal'),
    path('cadastrar/animal/', AnimalCreate.as_view(), name='cadastrar-animal'),
    path('editar/animal/<int:pk>/', AnimalUpdate.as_view(), name='editar-animal'),
    path('deletar/animal/<int:pk>/', AnimalDelete.as_view(), name='deletar-animal'),
    path('excluir/animal/<int:pk>/', AnimalDelete.as_view(), name='excluir-animal'),

    # Venda
    path('listar/vendas/', VendaList.as_view(), name='listar-venda'),
    path('cadastrar/venda/', VendaCreate.as_view(), name='cadastrar-venda'),
    path('detalhes/venda/<int:pk>/', VendaDetail.as_view(), name='detalhar-venda'),
]