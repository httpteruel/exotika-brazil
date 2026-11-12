import time
import os
from pathlib import Path
from django.conf import settings
from .models import ConfiguracaoIA, CotaMensalIA, RequisicaoIA, MensagemAssistente


class CotaExcedidaException(Exception):
    pass


def _estimar_tokens(texto: str) -> int:
    if not texto:
        return 0
    return max(1, len(texto) // 4)


def chamar_ia(
    prompt: str,
    usuario=None,
    system_instruction: str = "",
    origem: str = "Assistente Virtual",
    ignorar_cota: bool = False,
) -> dict:
    """
    Porta de entrada ÚNICA para chamadas de IA em todo o projeto Exotika Brazil.
    Retorna um dict com: {'sucesso': bool, 'resposta': str, 'tokens': int, 'erro': str}
    """
    config = ConfiguracaoIA.get_ativa()
    cota = None

    # 1. Verificação de Cota Mensal por Usuário
    if usuario and usuario.is_authenticated and not ignorar_cota:
        cota = CotaMensalIA.obter_ou_criar_atual(usuario)
        if cota.tokens_restantes <= 0:
            RequisicaoIA.objects.create(
                usuario=usuario,
                origem=origem,
                modelo_utilizado=config.modelo,
                prompt_enviado=prompt,
                status='COTA_EXCEDIDA',
                mensagem_erro='Cota mensal de tokens esgotada para este usuário.'
            )
            return {
                'sucesso': False,
                'resposta': '',
                'tokens': 0,
                'erro': f'Sua cota mensal de {cota.limite_tokens} tokens foi atingida. Contate o administrador.'
            }

    inicio = time.time()
    tokens_in = _estimar_tokens(system_instruction + "\n" + prompt)
    tokens_out = 0
    resposta_texto = ""

    try:
        if config.provedor == 'MOCK':
            time.sleep(0.3)
            resposta_texto = (
                f"**[Resposta Simulada - Exotika AI]**\n\n"
                f"Recebi sua solicitação: *\"{prompt[:120]}\"*.\n"
                f"O motor está operando em modo de simulação local."
            )
            tokens_out = _estimar_tokens(resposta_texto)
        else:
            try:
                from google import genai
                from google.genai import types
            except ImportError:
                raise ImportError("Pacote 'google-genai' não instalado. Execute: pip install google-genai")

            api_key = config.api_key.strip() or os.environ.get('GEMINI_API_KEY', '')
            if not api_key:
                raise ValueError("Nenhuma API Key configurada na tela de Configuração de IA.")

            client = genai.Client(api_key=api_key)
            gen_config = types.GenerateContentConfig(
                temperature=config.temperatura,
                max_output_tokens=config.max_tokens_resposta,
                system_instruction=system_instruction if system_instruction else None,
            )

            response = client.models.generate_content(
                model=config.modelo,
                contents=prompt,
                config=gen_config,
            )

            resposta_texto = response.text or ""

            if getattr(response, 'usage_metadata', None):
                tokens_in = getattr(response.usage_metadata, 'prompt_token_count', tokens_in) or tokens_in
                tokens_out = getattr(response.usage_metadata, 'candidates_token_count', 0) or _estimar_tokens(resposta_texto)
            else:
                tokens_out = _estimar_tokens(resposta_texto)

        total_tokens = tokens_in + tokens_out
        tempo_ms = int((time.time() - inicio) * 1000)

        if cota:
            cota.tokens_consumidos += total_tokens
            cota.save()

        RequisicaoIA.objects.create(
            usuario=usuario if (usuario and usuario.is_authenticated) else None,
            origem=origem,
            modelo_utilizado=config.modelo,
            prompt_enviado=prompt,
            resposta_recebida=resposta_texto,
            tokens_entrada=tokens_in,
            tokens_saida=tokens_out,
            total_tokens=total_tokens,
            tempo_resposta_ms=tempo_ms,
            status='SUCESSO',
        )

        return {
            'sucesso': True,
            'resposta': resposta_texto,
            'tokens': total_tokens,
            'tempo_ms': tempo_ms,
            'erro': ''
        }

    except Exception as exc:
        tempo_ms = int((time.time() - inicio) * 1000)
        erro_str = str(exc)

        RequisicaoIA.objects.create(
            usuario=usuario if (usuario and usuario.is_authenticated) else None,
            origem=origem,
            modelo_utilizado=config.modelo,
            prompt_enviado=prompt,
            tokens_entrada=tokens_in,
            tokens_saida=0,
            total_tokens=tokens_in,
            tempo_resposta_ms=tempo_ms,
            status='ERRO',
            mensagem_erro=erro_str,
        )

        return {
            'sucesso': False,
            'resposta': '',
            'tokens': 0,
            'tempo_ms': tempo_ms,
            'erro': erro_str
        }


def _carregar_contexto_projeto() -> str:
    caminho = Path(settings.BASE_DIR) / 'contexto_projeto.md'
    if caminho.exists():
        return caminho.read_text(encoding='utf-8')
    return "Sistema Exotika Brazil - Gestão de Animais Exóticos e Insumos."


def consultar_assistente_virtual(usuario, pergunta: str) -> dict:
    """
    Salva a pergunta do usuário, recupera apenas as últimas 5 mensagens do histórico
    (janela deslizante), monta as instruções com limites rígidos + contexto_projeto.md
    e aciona exclusivamente a porta de entrada única `chamar_ia`.
    """
    # 1. Grava a pergunta atual do usuário no histórico
    MensagemAssistente.objects.create(
        usuario=usuario,
        papel='user',
        conteudo=pergunta
    )

    # 2. Recupera apenas as últimas 5 mensagens do usuário (janela deslizante de 5)
    ultimas_5 = list(
        MensagemAssistente.objects.filter(usuario=usuario).order_by('-criado_em')[:5]
    )
    ultimas_5.reverse()

    historico_formatado = "\n".join(
        f"{'Usuário' if m.papel == 'user' else 'Assistente'}: {m.conteudo}"
        for m in ultimas_5
    )

    # 3. Monta System Instruction com contexto do projeto e limites explícitos
    contexto_md = _carregar_contexto_projeto()
    system_instruction = (
        "Você é o Assistente Oficial do sistema Exotika Brazil.\n"
        "Responda em português do Brasil usando formatação Markdown clara e objetiva.\n\n"
        "=== LIMITES E DIRETRIZES OBRIGATÓRIAS ===\n"
        "1. Responda APENAS sobre o funcionamento do sistema Exotika Brazil, manejo básico/legalização "
        "de animais exóticos e dúvidas sobre os cadastros e vendas da plataforma.\n"
        "2. Se o usuário perguntar sobre assuntos totalmente fora desse escopo (programação genérica, "
        "política, receitas culinárias, etc.), recuse educadamente e redirecione para o sistema.\n"
        "3. Nunca invente dados financeiros, registros de banco de dados ou licenças do IBAMA inexistentes.\n"
        "4. Não prescreva medicamentos veterinários; oriente sempre a consulta a um médico-veterinário especializado.\n"
        "5. Mantenha respostas concisas e bem estruturadas.\n\n"
        "=== CONTEXTO DO SISTEMA ===\n"
        f"{contexto_md}"
    )

    prompt_com_janela = (
        "Histórico recente da conversa (janela das últimas 5 mensagens):\n"
        f"{historico_formatado}\n\n"
        "Responda à última mensagem do Usuário acima."
    )

    # 4. Aciona a porta de entrada única chamar_ia
    resultado = chamar_ia(
        prompt=prompt_com_janela,
        usuario=usuario,
        system_instruction=system_instruction,
        origem="Assistente Virtual",
    )

    # 5. Se obteve sucesso, persiste a resposta do assistente no histórico
    if resultado['sucesso']:
        MensagemAssistente.objects.create(
            usuario=usuario,
            papel='assistant',
            conteudo=resultado['resposta']
        )

    return resultado