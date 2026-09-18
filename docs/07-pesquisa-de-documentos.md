# Etapa 7 — Pesquisa e ordenação de documentos

> **Objetivo:** permitir localizar um documento pelo nome e escolher a ordem em
> que os documentos aparecem na tela do cliente.

Última etapa do sistema.

---

## Requisitos de início

| # | Requisito | Como verificar |
| --- | --- | --- |
| RI-7.1 | [Etapa 6](06-inspecao-do-documento.md) concluída | Todos os critérios `RFim-6.x` atendidos |
| RI-7.2 | Um cliente com vários documentos cadastrados | Ter ao menos 5 documentos, de nomes e tamanhos diferentes |
| RI-7.3 | Campo `tamanho` preenchido nos documentos com arquivo | Conferir no painel admin |

> Documentos criados antes da Etapa 5 podem estar com `tamanho` vazio. Se isso
> acontecer, reenvie-os ou preencha o campo pelo admin — senão a ordenação por
> tamanho fica com resultados estranhos.

---

## Requisitos funcionais

### RF-7.1 — Barra de controles

No topo da seção Documentos, uma barra com:

- **Campo de busca**, com o texto de apoio "Buscar documento pelo nome"
- **Seletor de ordem**, com três opções
- Botão **Limpar**, visível apenas quando houver busca ou ordem diferente do
  padrão

A barra fica abaixo do título da seção e acima da grade de cards. O botão
"Enviar Documento" continua ao lado do título, como definido na
[Etapa 5](05-envio-de-documentos.md).

### RF-7.2 — Busca por nome

- A busca é feita sobre o campo `nome` do documento.
- É **parcial**: buscar `nota` encontra `Nota fiscal 2024`.
- **Ignora maiúsculas e minúsculas** (`icontains`).
- A descrição não entra na busca.

### RF-7.3 — Ordenação

| Opção | Rótulo na tela | Ordenação |
| --- | --- | --- |
| `envio` (padrão) | Ordem de envio | `enviado_em` crescente |
| `nome` | Ordem alfabética | `nome` crescente, ignorando maiúsculas |
| `tamanho` | Tamanho | `tamanho` **decrescente**, do maior para o menor |

Regras de desempate e casos especiais:

- Documentos do tipo URL não têm tamanho. Na ordenação por tamanho, eles vão
  para o **fim** da lista, independentemente da direção.
- Empates são desfeitos por `enviado_em`, para que a ordem seja sempre a mesma
  entre um carregamento e outro.

### RF-7.4 — Estado na URL

Busca e ordem viajam na **querystring** da tela do cliente:

```
/clientes/3/?q=nota&ordem=nome
```

Isso traz três benefícios:

1. O resultado da busca pode ser copiado e compartilhado como link.
2. O botão "voltar" do navegador funciona como o usuário espera.
3. Após enviar, editar ou excluir um documento, o redirecionamento preserva a
   busca em andamento.

A filtragem acontece **no banco de dados**, na view, e não no JavaScript.

> **Decisão D-7.1 — filtrar no servidor.** Filtrar no navegador daria uma
> resposta instantânea, mas só funcionaria sobre os documentos já carregados na
> página e deixaria o estado fora da URL. Filtrar na view é o caminho que
> continua correto quando a lista cresce e ganha paginação.

### RF-7.5 — Valores inválidos

- `ordem` com um valor fora da lista (`?ordem=qualquer`) é tratado como o padrão
  `envio`, sem erro.
- `q` vazio ou só com espaços é ignorado: mostra todos os documentos.
- Os valores digitados permanecem visíveis nos campos após a busca — o campo
  mostra o termo pesquisado e o seletor mostra a ordem escolhida.

### RF-7.6 — Resultado vazio

Quando a busca não encontra nada, a seção exibe uma mensagem específica —
*"Nenhum documento encontrado para «termo»."* — com um atalho para limpar a
busca.

Essa mensagem é **diferente** do estado vazio de "nenhum documento enviado
ainda": uma diz que não há documentos, a outra que a busca não encontrou nada.
Confundir as duas faz o usuário achar que perdeu os arquivos.

### RF-7.7 — Contagem

Ao lado do título da seção, o número de documentos exibidos. Quando há busca
ativa, o formato mostra os dois números: `3 de 12 documentos`.

### RF-7.8 — Envio do formulário

A barra é um `<form method="get">` apontando para a própria tela do cliente.

- Enviar o campo de busca com `Enter` aplica a pesquisa.
- Trocar a opção do seletor aplica a ordenação imediatamente (`submit` via
  JavaScript no evento `change`).
- Sem JavaScript, um botão **Aplicar** garante o mesmo resultado — a tela
  continua utilizável.

---

## Arquivos envolvidos

| Arquivo | O que muda |
| --- | --- |
| `core/views.py` | `cliente_detalhe` lê `q` e `ordem` e monta o `queryset`; as views de documento preservam a querystring no redirecionamento |
| `templates/core/cliente_detalhe.html` | Barra de busca e ordenação, contagem e mensagem de resultado vazio |
| `static/js/main.js` | Envio automático do formulário ao trocar a ordem |
| `static/css/styles.css` | Estilos da barra de controles |

---

## Requisitos de fim

| # | Critério de aceite | Como verificar |
| --- | --- | --- |
| RFim-7.1 | O campo de busca aparece no topo da seção Documentos | Conferir visualmente |
| RFim-7.2 | Buscar um termo filtra os cards | Buscar parte de um nome |
| RFim-7.3 | A busca ignora maiúsculas e minúsculas | Buscar `NOTA` e `nota` com o mesmo resultado |
| RFim-7.4 | A busca encontra pedaços do nome | Buscar `fisc` e achar `Nota fiscal` |
| RFim-7.5 | Uma busca sem resultados exibe a mensagem específica | Buscar `zzzzz` |
| RFim-7.6 | A ordem alfabética funciona | Selecionar "Ordem alfabética" |
| RFim-7.7 | A ordem de envio funciona e é o padrão | Recarregar a tela sem querystring |
| RFim-7.8 | A ordem por tamanho funciona, com as URLs ao final | Selecionar "Tamanho" |
| RFim-7.9 | Busca e ordem funcionam ao mesmo tempo | Buscar e ordenar; conferir a URL `?q=…&ordem=…` |
| RFim-7.10 | O termo buscado continua visível no campo | Conferir após a busca |
| RFim-7.11 | O botão Limpar volta ao estado padrão | Clicar em Limpar |
| RFim-7.12 | A contagem confere com o número de cards | Conferir os dois números |
| RFim-7.13 | Enviar um documento durante uma busca mantém a busca ativa | Buscar, enviar e conferir a URL |
| RFim-7.14 | `?ordem=qualquer` não quebra a tela | Digitar a URL à mão |
| RFim-7.15 | Clicar em um card durante a busca abre a inspeção normalmente | Buscar e clicar |

---

## Sistema concluído

Com esta etapa, o sistema atende ao escopo completo:

| Etapa | Entrega |
| --- | --- |
| [00](00-ambiente.md) | Ambiente rodando em `localhost:8000` |
| [01](01-tela-principal.md) | Tela principal e navegação |
| [02](02-cadastro-de-clientes.md) | Cadastro manual de clientes |
| [03](03-busca-por-cnpj.md) | Preenchimento automático via ReceitaWS |
| [04](04-tela-do-cliente.md) | Tela do cliente, edição e exclusão |
| [05](05-envio-de-documentos.md) | Envio de documentos |
| [06](06-inspecao-do-documento.md) | Inspeção, download, edição e exclusão de documentos |
| [07](07-pesquisa-de-documentos.md) | Pesquisa e ordenação |

---

**Etapa anterior:** [06 — Inspeção do documento](06-inspecao-do-documento.md)
