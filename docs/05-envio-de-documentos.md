# Etapa 5 — Envio de documentos

> **Objetivo:** permitir anexar documentos a um cliente — um arquivo PNG, JPG ou
> PDF, ou uma URL — e exibi-los como cards na tela do cliente.

---

## Requisitos de início

| # | Requisito | Como verificar |
| --- | --- | --- |
| RI-5.1 | [Etapa 4](04-tela-do-cliente.md) concluída | Todos os critérios `RFim-4.x` atendidos |
| RI-5.2 | Tela do cliente com a seção "Documentos" vazia | Abrir `/clientes/<pk>/` |
| RI-5.3 | `MEDIA_URL` e `MEDIA_ROOT` configurados | Conferir `config/settings.py` |
| RI-5.4 | Django servindo arquivos de mídia em desenvolvimento | Conferir o bloco `if settings.DEBUG` em `config/urls.py` |

> `MEDIA_ROOT` aponta para `media/`, que já está no `.gitignore` — arquivos
> enviados durante o minicurso não vão para o repositório.

---

## Modelo de dados

### Documento

| Campo | Tipo | Obrigatório | Observações |
| --- | --- | --- | --- |
| `cliente` | `ForeignKey(Cliente, on_delete=CASCADE, related_name="documentos")` | Sim | Excluir o cliente exclui seus documentos |
| `nome` | `CharField(200)` | Sim | Como o documento aparece no card |
| `descricao` | `TextField(blank=True)` | Não | Texto livre |
| `arquivo` | `FileField(upload_to="documentos/%Y/%m/", blank=True)` | Condicional | PNG, JPG/JPEG ou PDF |
| `url` | `URLField(blank=True)` | Condicional | Alternativa ao arquivo |
| `tamanho` | `PositiveIntegerField(null=True, blank=True)` | — | Tamanho em bytes; nulo quando for URL |
| `enviado_em` | `DateTimeField(auto_now_add=True)` | — | Define a ordem de exibição |

**Regras do modelo**

- `Meta.ordering = ["enviado_em"]` — os documentos aparecem na **ordem de
  envio**, do mais antigo para o mais novo.
- `__str__` devolve o `nome`.
- Propriedade `tipo`, derivada do conteúdo: `"png"`, `"jpg"`, `"pdf"` ou
  `"url"`. É ela que decide o ícone do card e a pré-visualização da
  [Etapa 6](06-inspecao-do-documento.md).
- `tamanho` é preenchido no `save()` a partir de `arquivo.size`, para que a
  ordenação por tamanho da [Etapa 7](07-pesquisa-de-documentos.md) não precise
  tocar o disco.

> **Decisão D-5.1 — arquivo OU url, nunca os dois.** Um documento tem exatamente
> uma origem. O formulário valida essa regra: nenhum dos dois preenchido é erro,
> os dois preenchidos também. Isso mantém a pré-visualização da Etapa 6 sem
> ambiguidade.

> **Decisão D-5.2 — por que guardar `tamanho` em coluna.** Seria possível ler
> `documento.arquivo.size` na hora de ordenar, mas isso significa um acesso ao
> disco por documento e impede ordenar no banco. Guardar o número no momento do
> envio resolve os dois problemas.

---

## Requisitos funcionais

### RF-5.1 — Migração

```bash
python manage.py makemigrations
python manage.py migrate
```

Registrar `Documento` em `core/admin.py` junto com o `Cliente`.

### RF-5.2 — Botão "Enviar Documento"

Na tela do cliente, **ao lado do título** da seção Documentos, um botão
**Enviar Documento**. Ao ser clicado, abre um popup (modal).

### RF-5.3 — Popup de envio

O modal contém:

| Campo | Tipo | Obrigatório |
| --- | --- | --- |
| Nome | texto | Sim |
| Descrição | área de texto | Não |
| Arquivo | seletor de arquivo (`accept=".png,.jpg,.jpeg,.pdf"`) | Um dos dois |
| URL | texto | Um dos dois |

Com dois botões: **Confirmar** (ação primária) e **Cancelar**.

### RF-5.4 — Cancelar antes de confirmar

O usuário pode desistir a qualquer momento antes de confirmar:

- Um botão **Cancelar** fecha o modal e descarta tudo o que foi digitado.
- Depois de escolher um arquivo, aparece o nome do arquivo selecionado com um
  botão **Remover** ao lado, que limpa a seleção sem fechar o modal.
- O modal também fecha com `Esc` e com clique fora da caixa.
- Nada é enviado ao servidor enquanto o usuário não clicar em **Confirmar**.

### RF-5.5 — Envio e gravação

- Rota: `POST /clientes/<int:pk>/documentos/novo/` (nome:
  `core:documento_novo`).
- O formulário usa `enctype="multipart/form-data"` e inclui `{% csrf_token %}`.
- Gravação bem-sucedida → redireciona para a tela do cliente, onde o documento
  já aparece como card.
- Gravação inválida → a tela do cliente é reexibida com o modal aberto e as
  mensagens de erro visíveis.

### RF-5.6 — Validação do envio

| # | Regra | Mensagem |
| --- | --- | --- |
| V-1 | `nome` obrigatório | "Informe um nome para o documento." |
| V-2 | Arquivo **ou** URL preenchido | "Envie um arquivo ou informe uma URL." |
| V-3 | Nunca os dois ao mesmo tempo | "Escolha apenas uma origem: arquivo ou URL." |
| V-4 | Extensão em `.png`, `.jpg`, `.jpeg`, `.pdf` | "Formato não aceito. Envie PNG, JPG ou PDF." |
| V-5 | Arquivo de no máximo 10 MB | "O arquivo deve ter no máximo 10 MB." |
| V-6 | URL começando com `http://` ou `https://` | "Informe uma URL válida." |

A validação da extensão acontece **no servidor**. O atributo `accept` do campo
de arquivo é apenas uma conveniência da interface: ele filtra o que aparece na
janela de seleção, mas não impede o envio de outro tipo.

### RF-5.7 — Cards de documento

Cada documento vira um card na seção Documentos, exibindo:

- Ícone ou etiqueta do tipo (PNG, JPG, PDF ou LINK)
- Nome do documento
- Primeira linha da descrição, quando houver
- Data de envio (`dd/mm/aaaa`)
- Tamanho legível (`124 KB`, `2,3 MB`) — para URLs, exibir `—`

Os cards ficam em uma grade que se reorganiza em telas estreitas, sempre em
**ordem de envio**.

Nesta etapa o card ainda não é clicável; ele passa a abrir a inspeção na
[Etapa 6](06-inspecao-do-documento.md).

### RF-5.8 — Estado vazio

Enquanto o cliente não tiver documentos, a seção continua mostrando o estado
vazio da Etapa 4.

---

## Arquivos envolvidos

| Arquivo | O que muda |
| --- | --- |
| `core/models.py` | Modelo `Documento` |
| `core/migrations/` | Nova migração |
| `core/forms.py` | `DocumentoForm`, com as validações V-1 a V-6 |
| `core/admin.py` | Registro do `Documento` |
| `core/urls.py` | Rota `clientes/<int:pk>/documentos/novo/` |
| `core/views.py` | View `documento_novo`; `cliente_detalhe` passa a enviar os documentos ao template |
| `templates/core/cliente_detalhe.html` | Botão, modal de envio e grade de cards |
| `static/js/main.js` | Modal de envio, nome do arquivo escolhido e botão Remover |
| `static/css/styles.css` | Estilos dos cards e do formulário dentro do modal |

---

## Requisitos de fim

| # | Critério de aceite | Como verificar |
| --- | --- | --- |
| RFim-5.1 | O botão "Enviar Documento" aparece ao lado do título da seção | Conferir visualmente |
| RFim-5.2 | O botão abre o modal com nome, descrição, arquivo e URL | Clicar no botão |
| RFim-5.3 | Enviar um PNG cria o card na tela do cliente | Enviar uma imagem |
| RFim-5.4 | Enviar um PDF cria o card | Enviar um PDF |
| RFim-5.5 | Cadastrar uma URL cria o card | Informar `https://exemplo.com.br` |
| RFim-5.6 | Enviar um `.docx` é recusado com mensagem clara | Tentar enviar |
| RFim-5.7 | Enviar sem nome é recusado | Deixar o nome vazio |
| RFim-5.8 | Enviar sem arquivo e sem URL é recusado | Preencher só o nome |
| RFim-5.9 | Preencher arquivo **e** URL é recusado | Preencher os dois |
| RFim-5.10 | Cancelar fecha o modal sem gravar nada | Preencher tudo e cancelar |
| RFim-5.11 | Remover o arquivo escolhido limpa a seleção sem fechar o modal | Escolher e remover |
| RFim-5.12 | Os documentos aparecem na ordem de envio | Enviar três e conferir a sequência |
| RFim-5.13 | O arquivo foi gravado em disco | Conferir a pasta `media/documentos/` |
| RFim-5.14 | Excluir o cliente remove seus documentos do banco | Excluir e conferir no admin |

---

**Etapa anterior:** [04 — Tela do cliente](04-tela-do-cliente.md) ·
**Próxima etapa:** [06 — Inspeção do documento](06-inspecao-do-documento.md)
