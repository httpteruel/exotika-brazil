import django_filters
from django import forms
from .models import Animal, Especie, CategoriaProduto, Produto


class AnimalFilter(django_filters.FilterSet):
    microchip_anilha = django_filters.CharFilter(
        field_name='microchip_anilha',
        lookup_expr='icontains',
        label='Microchip / Anilha',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Buscar por anilha ou chip...'})
    )

    especie = django_filters.ModelChoiceFilter(
        queryset=Especie.objects.all(),
        field_name='especie',
        lookup_expr='exact',
        label='Espécie',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    status = django_filters.ChoiceFilter(
        field_name='status',
        lookup_expr='exact',
        choices=Animal.STATUS_CHOICES if hasattr(Animal, 'STATUS_CHOICES') else [
            ('DISPONIVEL', 'Disponível'),
            ('VENDIDO', 'Vendido'),
            ('QUARENTENA', 'Em Quarentena'),
            ('OBITO', 'Óbito')
        ],
        label='Status',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    preco_min = django_filters.NumberFilter(
        field_name='preco',
        lookup_expr='gte',
        label='Preço Mínimo (R$)',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )

    preco_max = django_filters.NumberFilter(
        field_name='preco',
        lookup_expr='lte',
        label='Preço Máximo (R$)',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )

    class Meta:
        model = Animal
        fields = ['microchip_anilha', 'especie', 'status', 'preco_min', 'preco_max']


class ProdutoFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(
        field_name='nome',
        lookup_expr='icontains',
        label='Nome do Produto',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Buscar por produto...'})
    )

    categoria = django_filters.ModelChoiceFilter(
        queryset=CategoriaProduto.objects.all(),
        field_name='categoria',
        lookup_expr='exact',
        label='Categoria',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    preco_min = django_filters.NumberFilter(
        field_name='preco',
        lookup_expr='gte',
        label='Preço Mínimo (R$)',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )

    preco_max = django_filters.NumberFilter(
        field_name='preco',
        lookup_expr='lte',
        label='Preço Máximo (R$)',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )

    class Meta:
        model = Produto
        fields = ['nome', 'categoria', 'preco_min', 'preco_max']