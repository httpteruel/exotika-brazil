# AGENTS.md — Guia de Arquitetura e Regras do Projeto Exotika Brazil

Este documento define o contexto técnico, padrões de código e regras arquiteturais para agentes de IA que atuam no repositório **Exotika Brazil**.

## 1. Visão Geral do Sistema
Sistema web de gestão de criatório e comércio de animais exóticos e insumos, desenvolvido em **Django 5** com banco de dados **PostgreSQL (Neon.tech)** e deploy no **Google App Engine (GAE)**.

## 2. Estrutura de Apps
- `exotika/`: Configurações centrais (`settings.py`, `urls.py`, `wsgi.py`).
- `cadastros/`: Domínio principal (`Especie`, `CategoriaProduto`, `Fornecedor`, `Animal`, `Produto`, `Venda`, `ItemVenda`), filtros (`django-filter`) e views baseadas em classe (CBVs).
- `usuarios/`: Autenticação, registro e perfis de acesso.
- `ia/`: **Porta de entrada única** para integrações com LLMs, auditoria de tokens, cotas mensais e assistente virtual.

## 3. Regras Arquiteturais Obrigatórias
1. **Isolamento de IA:** Nenhuma view, model ou script fora do app `ia` pode importar SDKs de IA (como `google-genai` ou `openai`) diretamente. Toda chamada deve passar exclusivamente pela função `ia.services.chamar_ia()`.
2. **Controle de Acesso:**
   - Administradores: `is_superuser=True` ou pertencentes ao grupo `Administradores` (usar `AdminRequiredMixin`).
   - Usuários Comuns: Visualizam e manipulam apenas seus próprios registros (`usuario_cadastro` em `Animal` e `cliente` em `Venda`).
3. **Performance ORM:** Sempre utilizar `select_related` e `prefetch_related` em listagens para evitar queries N+1.
4. **Feedback ao Usuário:** Toda operação de criação, edição ou exclusão deve emitir feedback via `django.contrib.messages`.
5. **Frontend:** Bootstrap 5 (via CDN), FontAwesome 6 e jQuery (`jQuery Mask` e `Bootbox.js`). Templates estendem `templates/base.html`.

## 4. Skills Disponíveis
Consulte `.agents/skills/` para instruções detalhadas de execução:
- `.agents/skills/padrao-commits/SKILL.md`: Padronização de mensagens de commit (Conventional Commits).
- `.agents/skills/criar-crud-django/SKILL.md`: Padrão oficial para criação de novos CRUDs no projeto.
- `.agents/skills/auditoria-seguranca-django/SKILL.md`: Checklist de segurança, permissões e otimização ORM.