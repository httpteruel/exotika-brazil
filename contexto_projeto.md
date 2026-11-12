# Contexto do Sistema — Exotika Brazil

## 1. Sobre a Plataforma
O **Exotika Brazil** é um sistema de gestão especializada para criatórios e comércio legalizado de animais exóticos, silvestres autorizados pelo IBAMA e insumos veterinários/ambientais.

## 2. Módulos e Funcionalidades
- **Espécies:** Cadastro biológico com nome comum, nome científico, classe biológica (Répteis, Aves, Mamíferos, Anfíbios, Invertebrados) e indicador de obrigatoriedade de autorização do IBAMA.
- **Animais:** Controle individual por microchip ou anilha, vinculação à espécie e fornecedor, data de nascimento, sexo, preço e status (`DISPONIVEL`, `RESERVADO`, `VENDIDO`). Cada usuário comum visualiza e gerencia apenas os animais que cadastrou; administradores gerenciam todo o plantel.
- **Fornecedores:** Cadastro de criadouros e distribuidores legalizados (Razão Social, CNPJ/CPF, Licença IBAMA, contatos).
- **Produtos e Categorias:** Gestão de terrários, iluminação UVB, substratos, alimentação e suplementos com controle de estoque.
- **Vendas:** Registro de pedidos com múltiplos itens (animais e/ou produtos), baixa automática de estoque de produtos e alteração automática do status do animal para `VENDIDO`.
- **Governança de IA:** Controle de cota mensal de tokens por usuário, auditoria de requisições e assistente virtual integrado.

## 3. Fluxos de Navegação
- Menu **Cadastros**: Acesso rápido às listagens e formulários de Espécies, Fornecedores, Categorias, Animais e Produtos.
- Menu **Vendas**: Consulta de pedidos e criação de novas vendas.
- Menu **IA / Assistente**: Acesso ao Assistente Virtual, Meu Consumo de Tokens e (para administradores) Configuração de IA, Auditoria de Requisições e Cotas por Usuário.