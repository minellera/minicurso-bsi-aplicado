# Documentação e Specs

Esta pasta concentra toda a documentação do projeto e, principalmente, as
**especificações (specs)** que guiarão o desenvolvimento no minicurso.

A abordagem usada é o **SDD — Spec Driven Development**: primeiro escrevemos,
em Markdown, *o que* o sistema deve fazer; só depois escrevemos o código que
atende àquela especificação. A spec é a fonte da verdade — quando o
comportamento precisa mudar, a spec muda antes do código.

## Como esta pasta será organizada

Os arquivos serão adicionados ao longo do minicurso. A estrutura prevista é:

| Arquivo | Conteúdo |
| --- | --- |
| `00-problema.md` | Descrição do problema de negócio a ser resolvido |
| `01-visao-geral.md` | Visão geral da solução, público-alvo e objetivos |
| `02-requisitos.md` | Requisitos funcionais e não funcionais |
| `03-modelo-de-dados.md` | Entidades, atributos e relacionamentos |
| `04-telas.md` | Telas, fluxos de navegação e regras de interface |
| `05-criterios-de-aceite.md` | Como validar que cada requisito foi atendido |

> Os nomes acima são um ponto de partida. A lista definitiva será publicada
> aqui durante o minicurso.

## Convenções

- Um arquivo Markdown por tema, com prefixo numérico para manter a ordem.
- Requisitos identificados por código (`RF-01`, `RNF-01`) para poderem ser
  citados em commits, issues e prompts.
- Toda alteração de escopo entra primeiro na spec, depois no código.
