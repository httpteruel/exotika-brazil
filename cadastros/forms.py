from django import forms
from .models import Venda, ItemVenda, Animal, Produto

class VendaForm(forms.ModelForm):
    class Meta:
        model = Venda
        fields = ['cliente', 'status']

class ItemVendaForm(forms.ModelForm):
    class Meta:
        model = ItemVenda
        fields = ['produto', 'animal', 'quantidade', 'preco_unitario']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtra apenas os animais disponíveis para venda
        self.fields['animal'].queryset = Animal.objects.filter(status='DISPONIVEL')
        # Filtra apenas produtos com estoque maior que zero
        self.fields['produto'].queryset = Produto.objects.filter(quantidade_estoque__gt=0)