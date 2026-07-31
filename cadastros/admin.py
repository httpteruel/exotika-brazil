from django.contrib import admin
from .models import Especie, CategoriaProduto, Fornecedor, Animal, Produto, Venda, ItemVenda

@admin.register(Especie)
class EspecieAdmin(admin.ModelAdmin):
    list_display = ('nome_comum', 'nome_cientifico', 'classe_biologica', 'requer_autorizacao_ibama')
    search_fields = ('nome_comum', 'nome_cientifico')
    list_filter = ('classe_biologica', 'requer_autorizacao_ibama')

@admin.register(CategoriaProduto)
class CategoriaProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = ('razao_social', 'cnpj_cpf', 'licenca_ibama', 'telefone', 'email')
    search_fields = ('razao_social', 'cnpj_cpf')

@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ('especie', 'microchip_anilha', 'sexo', 'preco', 'status')
    list_filter = ('status', 'sexo', 'especie')
    search_fields = ('microchip_anilha', 'especie__nome_comum')

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'preco', 'quantidade_estoque')
    list_filter = ('categoria',)
    search_fields = ('nome',)

class ItemVendaInline(admin.TabularInline):
    model = ItemVenda
    extra = 1

@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'data_venda', 'status', 'valor_total')
    list_filter = ('status', 'data_venda')
    inlines = [ItemVendaInline]