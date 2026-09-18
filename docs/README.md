# Documentação e Specs

Esta pasta concentra toda a documentação do projeto e, principalmente, as
**especificações (specs)** que guiam o desenvolvimento no minicurso.

A abordagem usada é o **SDD — Spec Driven Development**: primeiro escrevemos,
em Markdown, *o que* o sistema deve fazer; só depois escrevemos o código que
atende àquela especificação. A spec é a fonte da verdade — quando o
comportamento precisa mudar, a spec muda antes do código.

## O sistema

**Empresa Maneira** — sistema de cadastro de clientes via CNPJ, com envio e
consulta de documentos por cliente.

## As etapas

O desenvolvimento está dividido em oito etapas, cada uma em um arquivo. As
etapas são **cumulativas**: cada uma depende da anterior estar funcionando.

| Arquivo | Etapa | Entrega |
| --- | --- | --- |
| [`00-ambiente.md`](00-ambiente.md) | Ambiente | Aplicação rodando em `localhost:8000` |
| [`01-tela-principal.md`](01-tela-principal.md) | Tela principal | Cabeçalho, navegação e lista (vazia) de clientes |
| [`02-cadastro-de-clientes.md`](02-cadastro-de-clientes.md) | Clientes | Modelo `Cliente` e cadastro manual |
| [`03-busca-por-cnpj.md`](03-busca-por-cnpj.md) | Busca por CNPJ | Preenchimento automático via API da ReceitaWS |
| [`04-tela-do-cliente.md`](04-tela-do-cliente.md) | Tela do cliente | Detalhe, edição e exclusão com confirmação |
| [`05-envio-de-documentos.md`](05-envio-de-documentos.md) | Documentos | Envio de PNG, JPG, PDF ou URL |
| [`06-inspecao-do-documento.md`](06-inspecao-do-documento.md) | Inspeção | Pré-visualização, download, edição e exclusão |
| [`07-pesquisa-de-documentos.md`](07-pesquisa-de-documentos.md) | Pesquisa | Busca por nome e ordenação |

## Como cada spec é organizada

Todas seguem a mesma estrutura:

1. **Objetivo** — o que a etapa entrega, em uma frase.
2. **Requisitos de início** (`RI-x.y`) — o que precisa estar pronto antes de
   começar. Serve para não iniciar uma etapa em cima de uma base quebrada.
3. **Requisitos funcionais** (`RF-x.y`) — o que deve ser construído.
4. **Arquivos envolvidos** — onde mexer.
5. **Requisitos de fim** (`RFim-x.y`) — os critérios de aceite. A etapa só está
   concluída quando todos forem verdadeiros.

## Convenções

- Um arquivo Markdown por etapa, com prefixo numérico para manter a ordem.
- Requisitos identificados pelo número da etapa: `RI-3.1` é o primeiro requisito
  de início da Etapa 3; `RF-5.2`, o segundo requisito funcional da Etapa 5. Use
  esses códigos em commits, issues e prompts.
- Decisões de projeto que não vêm diretamente do escopo aparecem marcadas como
  `D-x.y`, sempre com a justificativa ao lado.
- Toda alteração de escopo entra primeiro na spec, depois no código.
