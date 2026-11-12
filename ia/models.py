from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class ConfiguracaoIA(models.Model):
    PROVEDOR_CHOICES = [
        ('GEMINI', 'Google Gemini (google-genai)'),
        ('MOCK', 'Simulação Local (Teste sem API Key)'),
    ]

    nome = models.CharField(max_length=100, default='Configuração Principal Exotika AI')
    provedor = models.CharField(max_length=20, choices=PROVEDOR_CHOICES, default='GEMINI')
    modelo = models.CharField(
        max_length=80,
        default='gemini-2.5-flash',
        help_text='Ex: gemini-2.5-flash ou gemini-2.5-pro'
    )
    api_key = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Chave de API (API Key)',
        help_text='Chave secreta do provedor de IA'
    )
    temperatura = models.FloatField(
        default=0.4,
        help_text='Controla a criatividade (0.0 = determinístico, 1.0 = criativo)'
    )
    max_tokens_resposta = models.PositiveIntegerField(
        default=1024,
        verbose_name='Máximo de Tokens por Resposta'
    )
    cota_mensal_padrao = models.PositiveIntegerField(
        default=50000,
        verbose_name='Cota Mensal Padrão por Usuário (tokens)'
    )
    ativo = models.BooleanField(default=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Configuração de IA'
        verbose_name_plural = 'Configurações de IA'

    def __str__(self):
        return f"{self.nome} ({self.get_provedor_display()} - {self.modelo})"

    @classmethod
    def get_ativa(cls):
        config = cls.objects.filter(ativo=True).first()
        if not config:
            config = cls.objects.create(
                nome='Configuração Padrão',
                provedor='GEMINI',
                modelo='gemini-2.5-flash',
                ativo=True
            )
        return config


class CotaMensalIA(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cotas_ia')
    ano = models.PositiveIntegerField()
    mes = models.PositiveIntegerField()
    limite_tokens = models.PositiveIntegerField(default=50000)
    tokens_consumidos = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Cota Mensal de IA'
        verbose_name_plural = 'Cotas Mensais de IA'
        unique_together = ('usuario', 'ano', 'mes')
        ordering = ['-ano', '-mes', 'usuario__username']

    def __str__(self):
        return f"{self.usuario.username} - {self.mes:02d}/{self.ano} ({self.tokens_consumidos}/{self.limite_tokens})"

    @property
    def tokens_restantes(self):
        return max(0, self.limite_tokens - self.tokens_consumidos)

    @property
    def percentual_uso(self):
        if self.limite_tokens == 0:
            return 100
        return min(100, round((self.tokens_consumidos / self.limite_tokens) * 100, 1))

    @classmethod
    def obter_ou_criar_atual(cls, usuario):
        agora = timezone.now()
        config = ConfiguracaoIA.get_ativa()
        cota, _ = cls.objects.get_or_create(
            usuario=usuario,
            ano=agora.year,
            mes=agora.month,
            defaults={'limite_tokens': config.cota_mensal_padrao}
        )
        return cota


class RequisicaoIA(models.Model):
    STATUS_CHOICES = [
        ('SUCESSO', 'Sucesso'),
        ('ERRO', 'Erro'),
        ('COTA_EXCEDIDA', 'Cota Excedida'),
    ]

    usuario = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='requisicoes_ia'
    )
    origem = models.CharField(
        max_length=100,
        default='Assistente Virtual',
        help_text='Módulo ou funcionalidade que originou a chamada'
    )
    modelo_utilizado = models.CharField(max_length=80)
    prompt_enviado = models.TextField()
    resposta_recebida = models.TextField(blank=True)
    tokens_entrada = models.PositiveIntegerField(default=0)
    tokens_saida = models.PositiveIntegerField(default=0)
    total_tokens = models.PositiveIntegerField(default=0)
    tempo_resposta_ms = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SUCESSO')
    mensagem_erro = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Auditoria de Requisição IA'
        verbose_name_plural = 'Auditoria de Requisições IA'
        ordering = ['-criado_em']

    def __str__(self):
        user_str = self.usuario.username if self.usuario else 'Sistema'
        return f"[{self.criado_em:%d/%m/%Y %H:%M}] {user_str} - {self.origem} ({self.total_tokens} tokens)"

class MensagemAssistente(models.Model):
    PAPEL_CHOICES = [
        ('user', 'Usuário'),
        ('assistant', 'Assistente'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensagens_assistente')
    papel = models.CharField(max_length=15, choices=PAPEL_CHOICES)
    conteudo = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Mensagem do Assistente'
        verbose_name_plural = 'Mensagens do Assistente'
        ordering = ['criado_em']

    def __str__(self):
        return f"[{self.usuario.username} - {self.papel}] {self.conteudo[:50]}"