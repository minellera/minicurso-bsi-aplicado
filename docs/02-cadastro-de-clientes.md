# Etapa 2 — Estrutura e cadastro de clientes

> **Objetivo:** criar a entidade **Cliente** no banco de dados e a tela de
> cadastro manual, de forma que um cliente cadastrado passe a aparecer na lista
> da tela principal.

É aqui que o sistema deixa de ser uma casca visual e passa a guardar dados.

---

## Requisitos de início

| # | Requisito | Como verificar |
| --- | --- | --- |
| RI-2.1 | [Etapa 1](01-tela-principal.md) concluída | Todos os critérios `RFim-1.x` atendidos |
| RI-2.2 | Tela principal com seção de clientes e botão "Cadastrar Novo Cliente" | Conferir visualmente |
| RI-2.3 | Banco de dados criado e migrações em dia | `python manage.py migrate` sem pendências |

---

## Modelo de dados

### Cliente

| Campo | Tipo | Obrigatório | Observações |
| --- | --- | --- | --- |
| `nome` | `CharField(200)` | Sim | Razão social ou nome do cliente |
| `cnpj` | `CharField(18)` | Não | Formato `00.000.000/0000-00`; usado na [Etapa 3](03-busca-por-cnpj.md) |
| `porte` | `CharField(40)` com `choices` | Não | `MICRO EMPRESA`, `EMPRESA DE PEQUENO PORTE`, `DEMAIS` |
| `abertura` | `DateField` | Não | Data de abertura da empresa |
| `rua` | `CharField(200)` | Não | Logradouro |
| `numero` | `CharField(20)` | Não | Texto, não número — existe `S/N` |
| `cidade` | `CharField(120)` | Não | Município |
| `estado` | `CharField(2)` | Não | Sigla da UF, em maiúsculas |
| `cep` | `CharField(9)` | Não | Formato `00000-000` |
| `criado_em` | `DateTimeField(auto_now_add=True)` | — | Preenchido pelo Django |
| `atualizado_em` | `DateTimeField(auto_now=True)` | — | Preenchido pelo Django |

**Regras do modelo**

- `__str__` devolve o `nome` — é o que aparece no painel admin.
- `Meta.ordering = ["nome"]` — a listagem sai em ordem alfabética.
- Apenas `nome` é obrigatório. Os demais campos são opcionais para que um
  cadastro manual incompleto não trave o fluxo do minicurso.

> **Decisão D-2.1 — por que existe o campo `cnpj`.** O escopo da Etapa 2 lista
> nome, porte, abertura e endereço. O campo `cnpj` é acrescentado porque o
> subtítulo do sistema ("cadastro de clientes via CNPJ") e a
> [Etapa 3](03-busca-por-cnpj.md) dependem dele. Ele é **opcional**, então não
> atrapalha o cadastro manual.

> **Decisão D-2.2 — valores de `porte`.** Os três valores escolhidos são
> exatamente os devolvidos pela API da ReceitaWS. Isso faz o preenchimento
> automático da Etapa 3 virar uma atribuição direta, sem tabela de conversão.

---

## Requisitos funcionais

### RF-2.1 — Migração do modelo

Após criar o modelo em `core/models.py`:

```bash
python manage.py makemigrations
python manage.py migrate
```

A migração gerada é versionada junto com o código (fica em `core/migrations/`).

### RF-2.2 — Registro no painel admin

O modelo `Cliente` é registrado em `core/admin.py`, com `list_display` exibindo
nome, CNPJ, porte e cidade. Serve para conferir os dados durante o
desenvolvimento.

### RF-2.3 — Tela de cadastro

Nova rota `/clientes/novo/` (nome: `core:cliente_novo`), com um formulário
(`ClienteForm`, um `ModelForm`) contendo todos os campos do cliente:

- Nome, CNPJ, Porte (lista de seleção), Abertura (campo de data)
- Endereço: CEP, Rua, Número, Cidade, Estado

O formulário é enviado por `POST` e inclui `{% csrf_token %}`.

### RF-2.4 — O botão "Cadastrar Novo Cliente" passa a funcionar

Na tela principal, o botão criado na Etapa 1 passa a apontar para
`{% url 'core:cliente_novo' %}`.

### RF-2.5 — Gravação e retorno

- Formulário válido → o cliente é salvo e o usuário é **redirecionado para a
  tela principal**, onde o novo cliente já aparece na lista.
- Formulário inválido → a tela de cadastro é reexibida com os dados digitados
  preservados e as mensagens de erro ao lado dos campos.
- A tela de cadastro tem um botão **Cancelar**, que volta para a tela principal
  sem gravar nada.

### RF-2.6 — Listagem na tela principal

A view `index` passa a buscar os clientes do banco (`Cliente.objects.all()`) e a
seção de clientes exibe, para cada um:

- Nome
- CNPJ (quando houver)
- Cidade e estado (quando houver)
- Porte (quando houver)

O estado vazio da Etapa 1 continua aparecendo quando não há nenhum cliente.

### RF-2.7 — Validação de dados

| Campo | Regra |
| --- | --- |
| `nome` | Obrigatório; não pode ser só espaços |
| `cnpj` | Se preenchido, precisa ter 14 dígitos; é formatado como `00.000.000/0000-00` antes de salvar |
| `estado` | Se preenchido, exatamente 2 letras, gravadas em maiúsculas |
| `cep` | Se preenchido, 8 dígitos; formatado como `00000-000` antes de salvar |

A normalização (tirar pontuação, aplicar máscara, deixar a UF em maiúsculas)
acontece nos métodos `clean_<campo>()` do formulário — assim vale tanto para o
cadastro manual quanto para o preenchimento automático da Etapa 3.

---

## Arquivos envolvidos

| Arquivo | O que muda |
| --- | --- |
| `core/models.py` | Modelo `Cliente` |
| `core/migrations/` | Migração gerada por `makemigrations` |
| `core/forms.py` | **Novo** — `ClienteForm` |
| `core/admin.py` | Registro do `Cliente` |
| `core/urls.py` | Rota `clientes/novo/` |
| `core/views.py` | `index` lista clientes; nova view `cliente_novo` |
| `templates/core/index.html` | Lista real de clientes |
| `templates/core/cliente_form.html` | **Novo** — tela de cadastro |
| `static/css/styles.css` | Estilos de formulário e da lista de clientes |

---

## Requisitos de fim

| # | Critério de aceite | Como verificar |
| --- | --- | --- |
| RFim-2.1 | A tabela do cliente existe no banco | `python manage.py migrate` sem migrações pendentes |
| RFim-2.2 | O botão "Cadastrar Novo Cliente" leva para `/clientes/novo/` | Clicar na tela principal |
| RFim-2.3 | O formulário exibe todos os campos previstos | Conferir visualmente |
| RFim-2.4 | Um cadastro válido grava o cliente e volta para a tela principal | Cadastrar "Empresa Teste" e conferir a lista |
| RFim-2.5 | O cliente cadastrado aparece na lista com nome, cidade/estado e porte | Conferir a tela principal |
| RFim-2.6 | Enviar o formulário sem nome mostra erro e **não** grava | Submeter vazio |
| RFim-2.7 | O botão Cancelar volta para a tela principal sem gravar | Clicar em Cancelar |
| RFim-2.8 | O cliente aparece no painel admin | <http://localhost:8000/admin/> |
| RFim-2.9 | Após cadastrar, o estado vazio desaparece | Conferir a tela principal |

---

**Etapa anterior:** [01 — Tela principal](01-tela-principal.md) ·
**Próxima etapa:** [03 — Busca automática por CNPJ](03-busca-por-cnpj.md)
