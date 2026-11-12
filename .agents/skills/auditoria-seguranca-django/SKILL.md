---
name: auditoria-seguranca-django
description: Checklist de revisão de código, segurança, CSRF, XSS e otimização ORM antes de commits ou deploy.
---

# Skill: Auditoria de Código e Segurança Django

Antes de finalizar qualquer tarefa ou submeter código para revisão, valide os seguintes pontos:

1. **Proteção de Views:** Todas as views de escrita (`Create`, `Update`, `Delete`) exigem autenticação (`LoginRequiredMixin`) e verificação de papel (`AdminRequiredMixin` ou `DonoOuAdminRequiredMixin`)?
2. **Prevenção de N+1:** Listagens com `ForeignKey` usam `select_related()` e relações reversas/M2M usam `prefetch_related()`?
3. **Segurança Frontend (XSS e CSRF):**
   - Todos os formulários `POST` e requisições `AJAX` enviam o token `X-CSRFToken`?
   - Conteúdo dinâmico gerado por usuários ou pela IA é sanitizado (ex: `DOMPurify` no frontend ou `bleach` no backend) antes de ser injetado como HTML?
4. **Segredos e Credenciais:** Nenhuma chave de API (`GEMINI_API_KEY`, `OPENAI_API_KEY`) está hardcoded no código-fonte (devem ficar no banco de dados via model `ConfiguracaoIA` ou variáveis de ambiente).