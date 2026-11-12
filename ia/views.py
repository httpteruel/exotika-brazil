from django.views.generic import ListView, TemplateView, View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Sum, Count
from django.utils import timezone

from cadastros.views import AdminRequiredMixin
from .models import ConfiguracaoIA, CotaMensalIA, RequisicaoIA
from .forms import ConfiguracaoIAForm
from .services import chamar_ia


# ==============================================================================
# TELA 1: AUDITORIA DE REQUISIÇÕES
# ==============================================================================
class RequisicaoIAListView(LoginRequiredMixin, ListView):
    model = RequisicaoIA
    template_name = 'ia/requisicoes_list.html'
    context_object_name = 'requisicoes'
    paginate_by = 15

    def get_queryset(self):
        qs = RequisicaoIA.objects.select_related('usuario').all()
        if not (self.request.user.is_superuser or self.request.user.groups.filter(name='Administradores').exists()):
            qs = qs.filter(usuario=self.request.user)
        return qs


# ==============================================================================
# TELA 2: CONFIGURAÇÃO DE IA + TESTAR CONEXÃO
# ==============================================================================
class ConfiguracaoIAView(LoginRequiredMixin, AdminRequiredMixin, View):
    template_name = 'ia/configuracao_form.html'

    def get(self, request):
        config = ConfiguracaoIA.get_ativa()
        form = ConfiguracaoIAForm(instance=config)
        return render(request, self.template_name, {'form': form, 'config': config})

    def post(self, request):
        config = ConfiguracaoIA.get_ativa()
        form = ConfiguracaoIAForm(request.POST, instance=config)
        if form.is_valid():
            form.save()
            messages.success(request, "Configurações de Inteligência Artificial atualizadas com sucesso!")
            return redirect('ia-configuracao')
        return render(request, self.template_name, {'form': form, 'config': config})


class TestarConexaoIAView(LoginRequiredMixin, AdminRequiredMixin, View):
    def post(self, request):
        resultado = chamar_ia(
            prompt="Responda apenas com: 'Conexão estabelecida com sucesso no sistema Exotika Brazil!'",
            usuario=request.user,
            origem="Teste de Conexão (Admin)",
            ignorar_cota=True,
        )
        return JsonResponse(resultado)


# ==============================================================================
# TELA 3: IA POR USUÁRIO (GESTÃO DE COTAS E CONSUMO GLOBAL)
# ==============================================================================
class IAPorUsuarioView(LoginRequiredMixin, AdminRequiredMixin, View):
    template_name = 'ia/ia_por_usuario.html'

    def get(self, request):
        agora = timezone.now()
        usuarios = User.objects.all().order_by('username')
        dados_usuarios = []

        for u in usuarios:
            cota = CotaMensalIA.obter_ou_criar_atual(u)
            total_reqs = RequisicaoIA.objects.filter(
                usuario=u, criado_em__year=agora.year, criado_em__month=agora.month
            ).count()
            dados_usuarios.append({
                'usuario': u,
                'cota': cota,
                'total_reqs': total_reqs,
            })

        return render(request, self.template_name, {
            'dados_usuarios': dados_usuarios,
            'mes_atual': f"{agora.month:02d}/{agora.year}",
        })

    def post(self, request):
        cota_id = request.POST.get('cota_id')
        novo_limite = request.POST.get('limite_tokens')
        cota = get_object_or_404(CotaMensalIA, id=cota_id)
        try:
            cota.limite_tokens = max(0, int(novo_limite))
            cota.save()
            messages.success(request, f"Cota mensal de '{cota.usuario.username}' atualizada para {cota.limite_tokens} tokens.")
        except (ValueError, TypeError):
            messages.error(request, "Valor inválido para limite de tokens.")
        return redirect('ia-por-usuario')


# ==============================================================================
# TELA 4: MEU CONSUMO (VISÃO INDIVIDUAL DO USUÁRIO)
# ==============================================================================
class MeuConsumoIAView(LoginRequiredMixin, TemplateView):
    template_name = 'ia/meu_consumo.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cota = CotaMensalIA.obter_ou_criar_atual(self.request.user)
        ultimas_reqs = RequisicaoIA.objects.filter(usuario=self.request.user)[:10]
        stats = RequisicaoIA.objects.filter(usuario=self.request.user).aggregate(
            total_chamadas=Count('id'),
            total_tokens_historico=Sum('total_tokens')
        )
        context['cota'] = cota
        context['ultimas_reqs'] = ultimas_reqs
        context['total_chamadas'] = stats['total_chamadas'] or 0
        context['total_tokens_historico'] = stats['total_tokens_historico'] or 0
        return context

class AssistenteVirtualView(LoginRequiredMixin, View):
    template_name = 'ia/assistente.html'

    def get(self, request):
        historico = MensagemAssistente.objects.filter(usuario=request.user).order_by('criado_em')
        cota = CotaMensalIA.obter_ou_criar_atual(request.user)
        return render(request, self.template_name, {
            'historico': historico,
            'cota': cota,
        })

    def post(self, request):
        if request.POST.get('acao') == 'limpar':
            MensagemAssistente.objects.filter(usuario=request.user).delete()
            messages.success(request, "Histórico da conversa limpo com sucesso.")
        return redirect('ia-assistente')


class AssistentePerguntarAjaxView(LoginRequiredMixin, View):
    def post(self, request):
        try:
            if request.content_type == 'application/json':
                dados = json.loads(request.body)
                pergunta = dados.get('pergunta', '').strip()
            else:
                pergunta = request.POST.get('pergunta', '').strip()
        except json.JSONDecodeError:
            return JsonResponse({'sucesso': False, 'erro': 'Formato de requisição inválido.'}, status=400)

        if not pergunta:
            return JsonResponse({'sucesso': False, 'erro': 'Digite uma pergunta antes de enviar.'}, status=400)

        resultado = consultar_assistente_virtual(request.user, pergunta)
        cota = CotaMensalIA.obter_ou_criar_atual(request.user)
        resultado['tokens_restantes'] = cota.tokens_restantes
        return JsonResponse(resultado)