from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

# ------------------------------------------------------------------------------
# 1. ESPECIE (Categoria Taxonômica / Biológica)
# ------------------------------------------------------------------------------
class Especie(models.Model):
    CLASS_CHOICES = [
        ('REPTIL', 'Répteis'),
        ('ANFIBIO', 'Anfíbios'),
        ('AVE', 'Aves'),
        ('INVERTEBRADO', 'Invertebrados'),
    ]

    nome_comum = models.CharField(max_length=100, verbose_name="Nome Comum")
    nome_cientifico = models.CharField(max_length=150, verbose_name="Nome Científico", unique=True)
    classe_biologica = models.CharField(max_length=20, choices=CLASS_CHOICES, verbose_name="Classe Biológica")
    requer_autorizacao_ibama = models.BooleanField(default=True, verbose_name="Requer Autorização IBAMA?")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição / Cuidados Básicos")
    foto = models.ImageField(upload_to='especies/', blank=True, null=True, verbose_name="Foto / Ilustração")

    def __str__(self):
        return f"{self.nome_comum} ({self.nome_cientifico})"

    class Meta:
        verbose_name = "Espécie"
        verbose_name_plural = "Espécies"
        ordering = ['nome_comum']


# ------------------------------------------------------------------------------
# 2. CATEGORIA DE PRODUTO (Insumos)
# ------------------------------------------------------------------------------
class CategoriaProduto(models.Model):
    nome = models.CharField(max_length=100, unique=True, verbose_name="Nome da Categoria")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Categoria de Produto"
        verbose_name_plural = "Categorias de Produtos"
        ordering = ['nome']


# ------------------------------------------------------------------------------
# 3. FORNECEDOR / CRIATÓRIO PARCEIRO
# ------------------------------------------------------------------------------
class Fornecedor(models.Model):
    razao_social = models.CharField(max_length=150, verbose_name="Razão Social / Nome")
    cnpj_cpf = models.CharField(max_length=18, unique=True, verbose_name="CNPJ/CPF")
    licenca_ibama = models.CharField(max_length=50, blank=True, null=True, verbose_name="Número Licença IBAMA/CTF")
    telefone = models.CharField(max_length=20, verbose_name="Telefone")
    email = models.EmailField(verbose_name="E-mail")

    def __str__(self):
        return self.razao_social

    class Meta:
        verbose_name = "Fornecedor"
        verbose_name_plural = "Fornecedores"
        ordering = ['razao_social']


# ------------------------------------------------------------------------------
# 4. ANIMAL (Instância individual comercializável)
# ------------------------------------------------------------------------------
class Animal(models.Model):
    STATUS_CHOICES = [
        ('DISPONIVEL', 'Disponível'),
        ('RESERVADO', 'Reservado'),
        ('VENDIDO', 'Vendido'),
        ('QUARENTENA', 'Em Quarentena'),
    ]

    especie = models.ForeignKey(Especie, on_delete=models.PROTECT, related_name="animais", verbose_name="Espécie")
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.PROTECT, related_name="animais", verbose_name="Criatório/Fornecedor")
    microchip_anilha = models.CharField(max_length=50, unique=True, verbose_name="Nº Microchip / Anilha (Marcação)")
    data_nascimento = models.DateField(blank=True, null=True, verbose_name="Data de Nascimento / Eclosão")
    sexo = models.CharField(max_length=10, choices=[('M', 'Macho'), ('F', 'Fêmea'), ('I', 'Indeterminado')], default='I')
    preco = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name="Preço (R$)")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='DISPONIVEL', verbose_name="Status")
    foto = models.ImageField(upload_to='animais/', blank=True, null=True, verbose_name="Foto do Animal")

    def __str__(self):
        return f"{self.especie.nome_comum} - ID: {self.microchip_anilha}"

    class Meta:
        verbose_name = "Animal"
        verbose_name_plural = "Animais"


# ------------------------------------------------------------------------------
# 5. PRODUTO (Terrários, Rações, Iluminação, Equipamentos)
# ------------------------------------------------------------------------------
class Produto(models.Model):
    categoria = models.ForeignKey(CategoriaProduto, on_delete=models.PROTECT, related_name="produtos", verbose_name="Categoria")
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.SET_NULL, null=True, blank=True, related_name="produtos", verbose_name="Fornecedor")
    nome = models.CharField(max_length=150, verbose_name="Nome do Produto")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição Detalhada")
    preco = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name="Preço de Venda (R$)")
    quantidade_estoque = models.PositiveIntegerField(default=0, verbose_name="Quantidade em Estoque")
    imagem = models.ImageField(upload_to='produtos/', blank=True, null=True, verbose_name="Imagem do Produto")

    def __str__(self):
        return f"{self.nome} (Estoque: {self.quantidade_estoque})"

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"


# ------------------------------------------------------------------------------
# 6. VENDA / MOVIMENTAÇÃO (Cabeçalho do Movimento)
# ------------------------------------------------------------------------------
class Venda(models.Model):
    STATUS_VENDA = [
        ('EM_ABERTO', 'Em Aberto'),
        ('CONCLUIDA', 'Concluída'),
        ('CANCELADA', 'Cancelada'),
    ]

    cliente = models.ForeignKey(User, on_delete=models.PROTECT, related_name="compras", verbose_name="Cliente/Usuário")
    data_venda = models.DateTimeField(auto_now_add=True, verbose_name="Data/Hora da Venda")
    status = models.CharField(max_length=15, choices=STATUS_VENDA, default='EM_ABERTO', verbose_name="Status da Venda")
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Valor Total (R$)")

    def __str__(self):
        return f"Venda nº {self.id} - Cliente: {self.cliente.username}"

    class Meta:
        verbose_name = "Venda"
        verbose_name_plural = "Vendas"


# ------------------------------------------------------------------------------
# 7. ITEM DA VENDA (Detalhamento dos Itens do Movimento)
# ------------------------------------------------------------------------------
class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, related_name="itens", verbose_name="Venda")
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT, blank=True, null=True, verbose_name="Produto")
    animal = models.ForeignKey(Animal, on_delete=models.PROTECT, blank=True, null=True, verbose_name="Animal")
    quantidade = models.PositiveIntegerField(default=1, verbose_name="Quantidade")
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço Unitário (R$)")

    def __str__(self):
        item_nome = self.produto.nome if self.produto else f"Animal: {self.animal}"
        return f"{self.quantidade}x {item_nome} (Venda #{self.venda.id})"

    class Meta:
        verbose_name = "Item da Venda"
        verbose_name_plural = "Itens da Venda"