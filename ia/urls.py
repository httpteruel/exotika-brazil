from django.urls import path
from .views import (
    RequisicaoIAListView,
    ConfiguracaoIAView,
    TestarConexaoIAView,
    IAPorUsuarioView,
    MeuConsumoIAView,
    AssistenteVirtualView,
    AssistentePerguntarAjaxView,
)

urlpatterns = [
    path('assistente/', AssistenteVirtualView.as_view(), name='ia-assistente'),
    path('assistente/perguntar/', AssistentePerguntarAjaxView.as_view(), name='ia-assistente-perguntar'),
    path('requisicoes/', RequisicaoIAListView.as_view(), name='ia-requisicoes'),
    path('configuracao/', ConfiguracaoIAView.as_view(), name='ia-configuracao'),
    path('configuracao/testar/', TestarConexaoIAView.as_view(), name='ia-testar-conexao'),
    path('usuarios/', IAPorUsuarioView.as_view(), name='ia-por-usuario'),
    path('meu-consumo/', MeuConsumoIAView.as_view(), name='ia-meu-consumo'),
]