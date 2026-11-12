---
name: criar-crud-django
description: Define o padrão completo para criação de novos CRUDs (Model, View, URL e Template) no Exotika Brazil.
---

# Skill: Padrão de Criação de CRUD Django

Ao criar uma nova entidade no projeto **Exotika Brazil**, siga obrigatoriamente esta sequência:

1. **Model (`models.py`):**
   - Defina `verbose_name`, `verbose_name_plural` e `ordering` na classe `Meta`.
   - Implemente `__str__` legível.
   - Se o registro pertencer a um usuário, adicione `usuario_cadastro = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)`.

2. **Views (`views.py`):**
   - Utilize Class-Based Views (`ListView`/`FilterView`, `CreateView`, `UpdateView`, `DeleteView`).
   - Defina `paginate_by = 10` nas listagens.
   - Aplique `LoginRequiredMixin` + `AdminRequiredMixin` (ou `DonoOuAdminRequiredMixin`).
   - Adicione `SuccessMessageMixin` nas views de criação/edição e `messages.success()` no `delete()`.

3. **URLs (`urls.py`):**
   - Siga a convenção de nomenclatura: `listar-<entidade>`, `cadastrar-<entidade>`, `editar-<entidade>`, `excluir-<entidade>`.

4. **Templates (`templates/cadastros/`):**
   - Estenda `base.html`.
   - Use classes Bootstrap 5 (`table-hover`, `card shadow-sm`) e adicione `btn-bootbox-delete` nos links de exclusão.