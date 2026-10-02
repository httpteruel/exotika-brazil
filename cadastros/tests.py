from decimal import Decimal
from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Produto, Animal, CategoriaProduto, Especie, Fornecedor


class ProdutoCaixaBrancaTest(TestCase):
    """
    Testes de Caixa-Branca (Análise do Valor Limite - AVL) no Modelo Produto
    """

    def setUp(self):
        self.categoria = CategoriaProduto.objects.create(nome="Insumos Geral")

    def test_ct01_produto_preco_negativo_deve_falhar(self):
        """CT01: Preço -0.01 deve lançar ValidationError via MinValueValidator(0)"""
        produto = Produto(
            nome="Terrário MD",
            categoria=self.categoria,
            preco=Decimal('-0.01'),
            quantidade_estoque=10
        )
        with self.assertRaises(ValidationError):
            produto.full_clean()

    def test_ct02_produto_preco_zero_deve_passar(self):
        """CT02: Preço 0.00 deve ser aceito como válido"""
        produto = Produto(
            nome="Terrário MD",
            categoria=self.categoria,
            preco=Decimal('0.00'),
            quantidade_estoque=10
        )
        try:
            produto.full_clean()
        except ValidationError as e:
            self.fail(f"full_clean() lançou ValidationError para preço 0.00: {e}")

    def test_ct03_produto_preco_positivo_deve_passar(self):
        """CT03: Preço 0.01 deve ser aceito como válido"""
        produto = Produto(
            nome="Terrário MD",
            categoria=self.categoria,
            preco=Decimal('0.01'),
            quantidade_estoque=10
        )
        try:
            produto.full_clean()
        except ValidationError as e:
            self.fail(f"full_clean() lançou ValidationError para preço 0.01: {e}")

    def test_ct04_produto_estoque_negativo_deve_falhar(self):
        """CT04: Estoque -1 deve lançar ValidationError via PositiveIntegerField"""
        produto = Produto(
            nome="Terrário MD",
            categoria=self.categoria,
            preco=Decimal('10.00'),
            quantidade_estoque=-1
        )
        with self.assertRaises(ValidationError):
            produto.full_clean()

    def test_ct05_produto_estoque_zero_deve_passar(self):
        """CT05: Estoque 0 deve ser aceito como válido"""
        produto = Produto(
            nome="Terrário MD",
            categoria=self.categoria,
            preco=Decimal('10.00'),
            quantidade_estoque=0
        )
        try:
            produto.full_clean()
        except ValidationError as e:
            self.fail(f"full_clean() lançou ValidationError para estoque 0: {e}")

    def test_ct06_produto_estoque_positivo_deve_passar(self):
        """CT06: Estoque 1 deve ser aceito como válido"""
        produto = Produto(
            nome="Terrário MD",
            categoria=self.categoria,
            preco=Decimal('10.00'),
            quantidade_estoque=1
        )
        try:
            produto.full_clean()
        except ValidationError as e:
            self.fail(f"full_clean() lançou ValidationError para estoque 1: {e}")


class AnimalCaixaBrancaTest(TestCase):
    """
    Testes de Caixa-Branca (Análise do Valor Limite - AVL) no Modelo Animal
    """

    def setUp(self):
        self.especie = Especie.objects.create(
            nome_comum="Jiboia Arco-Íris",
            nome_cientifico="Epicrates cenchria",
            classe_biologica="REPTIL"
        )
        self.fornecedor = Fornecedor.objects.create(
            razao_social="Criatório Exótico Legal",
            cnpj_cpf="12.345.678/0001-90",
            telefone="44999999999",
            email="contato@criatorio.com"
        )

    def test_ct07_animal_preco_negativo_deve_falhar(self):
        """CT07: Preço -0.01 deve lançar ValidationError via MinValueValidator(0)"""
        animal = Animal(
            especie=self.especie,
            fornecedor=self.fornecedor,
            microchip_anilha="981000001234567",
            preco=Decimal('-0.01')
        )
        with self.assertRaises(ValidationError):
            animal.full_clean()

    def test_ct08_animal_preco_zero_deve_passar(self):
        """CT08: Preço 0.00 deve ser aceito como válido"""
        animal = Animal(
            especie=self.especie,
            fornecedor=self.fornecedor,
            microchip_anilha="981000001234568",
            preco=Decimal('0.00')
        )
        try:
            animal.full_clean()
        except ValidationError as e:
            self.fail(f"full_clean() lançou ValidationError para preço 0.00: {e}")

    def test_ct09_animal_preco_positivo_deve_passar(self):
        """CT09: Preço 0.01 deve ser aceito como válido"""
        animal = Animal(
            especie=self.especie,
            fornecedor=self.fornecedor,
            microchip_anilha="981000001234569",
            preco=Decimal('0.01')
        )
        try:
            animal.full_clean()
        except ValidationError as e:
            self.fail(f"full_clean() lançou ValidationError para preço 0.01: {e}")