---
name: padrao-commits
description: Padroniza mensagens de commit seguindo Conventional Commits em português para o projeto Exotika Brazil.
---

# Skill: Padronização de Mensagens de Commit

Sempre que gerar ou sugerir uma mensagem de commit para este repositório, siga rigorosamente o formato **Conventional Commits** em português:

## Formato
`<tipo>(<escopo>): <descrição curta no imperativo>`

## Tipos Permitidos
- `feat`: Nova funcionalidade (ex: `feat(ia): adiciona tela de auditoria de requisicoes`)
- `fix`: Correção de bug (ex: `fix(vendas): corrige calculo de estoque ao cancelar item`)
- `docs`: Alterações em documentação (`AGENTS.md`, `README.md`, `contexto_projeto.md`)
- `style`: Formatação, indentação ou ajustes visuais HTML/CSS sem alterar lógica
- `refactor`: Refatoração de código sem mudar comportamento externo
- `perf`: Melhoria de performance ou otimização de queries ORM
- `chore`: Atualização de dependências (`requirements.txt`), `app.yaml` ou configurações

## Regras
1. A primeira linha deve ter no máximo **72 caracteres**.
2. Não termine a linha de título com ponto final.
3. Use o verbo no imperativo (`adiciona`, `corrige`, `remove`, `atualiza`).
4. Se houver múltiplas alterações relevantes, adicione um corpo em tópicos (`- `) após uma linha em branco.