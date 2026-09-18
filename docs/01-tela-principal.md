# Etapa 1 — Tela principal

> **Objetivo:** substituir a tela de boas-vindas do ambiente base pela tela
> principal do sistema **Empresa Maneira**, com a barra de navegação que estará
> presente em todas as telas e a área que listará os clientes.

Nesta etapa ainda **não há banco de dados nem clientes reais**. Montamos a
estrutura visual e o estado vazio da listagem.

---

## Requisitos de início

| # | Requisito | Como verificar |
| --- | --- | --- |
| RI-1.1 | [Etapa 0](00-ambiente.md) concluída | Todos os critérios `RFim-0.x` atendidos |
| RI-1.2 | Servidor rodando em `localhost:8000` | A página inicial abre no navegador |
| RI-1.3 | Ambiente virtual ativado | O prefixo `(.venv)` aparece no terminal |

---

## Requisitos funcionais

### RF-1.1 — Barra de navegação global

Todas as telas do sistema exibem, no topo, uma barra de navegação fixa no
layout, contendo:

- Um **logotipo improvisado** do sistema no canto **esquerdo** — texto
  "Empresa Maneira" acompanhado de uma marca simples (por exemplo, um quadrado
  azul arredondado com as iniciais `EM`). Não é necessário arquivo de imagem.
- O logotipo é um **link** para a página inicial (`/`).

A barra vive em `templates/base.html`, de modo que qualquer template que estenda
`base.html` a herde automaticamente.

### RF-1.2 — Cabeçalho da tela principal

Abaixo da barra de navegação, a tela principal exibe:

- **Título:** `Empresa Maneira`
- **Subtítulo:** `Sistema de cadastro de clientes via CNPJ`

### RF-1.3 — Seção de clientes

Abaixo do cabeçalho, uma seção que lista os clientes já cadastrados.

- A seção tem um título (por exemplo, `Clientes`).
- Enquanto não houver clientes, exibe um **estado vazio** com uma mensagem
  amigável — algo como *"Nenhum cliente cadastrado ainda."*
- Nesta etapa, a lista é alimentada por uma **lista vazia** vinda da view. Não
  criamos modelos nem migrações agora; isso é feito na
  [Etapa 2](02-cadastro-de-clientes.md).

### RF-1.4 — Botão "Cadastrar Novo Cliente"

Na seção de clientes há um botão **Cadastrar Novo Cliente**, posicionado ao lado
do título da seção.

- Nesta etapa o botão **não executa nenhuma ação**. Ele existe, é visível e está
  estilizado como botão primário.
- O comportamento é implementado na [Etapa 2](02-cadastro-de-clientes.md).

### RF-1.5 — Identidade visual

O sistema adota um visual sóbrio, definido aqui e reutilizado em todas as etapas
seguintes:

| Item | Definição |
| --- | --- |
| Fundo da página | Branco (`#ffffff`) |
| Cor primária | Azul (`#1b5fbe`) — botões, links e logotipo |
| Azul escuro | `#123f80` — estados `hover` e títulos de destaque |
| Azul claro | `#eaf1fc` — fundos de apoio, chips e realces |
| Texto | `#1b1f24`; texto secundário `#5b6472` |
| Bordas | `#dde3ec`, cantos arredondados (`8px`–`12px`) |
| Tipografia | Simples, sem fontes externas: a pilha de fontes do sistema |

As cores ficam em variáveis CSS (`:root`) em `static/css/styles.css`, para que
uma mudança de paleta aconteça em um único lugar.

> **Decisão D-1.1 — sem modo escuro.** O ambiente base trazia um bloco
> `@media (prefers-color-scheme: dark)` com paleta verde. Como o escopo pede
> "fundo branco com cores azuis", esse bloco é **removido** nesta etapa.

---

## Arquivos envolvidos

| Arquivo | O que muda |
| --- | --- |
| `core/views.py` | View `index` passa a devolver a lista (vazia) de clientes |
| `templates/base.html` | Barra de navegação com o logotipo e link para `/` |
| `templates/core/index.html` | Cabeçalho, seção de clientes, estado vazio e botão |
| `static/css/styles.css` | Nova paleta branco/azul, estilos de botão, lista e estado vazio |

---

## Requisitos de fim

| # | Critério de aceite | Como verificar |
| --- | --- | --- |
| RFim-1.1 | A tela principal exibe o título "Empresa Maneira" e o subtítulo "Sistema de cadastro de clientes via CNPJ" | Abrir <http://localhost:8000/> |
| RFim-1.2 | A barra de navegação aparece no topo, com o logotipo à esquerda | Conferir visualmente |
| RFim-1.3 | Clicar no logotipo leva para `/` | Clicar e conferir a URL |
| RFim-1.4 | Existe uma seção de clientes com estado vazio visível | Conferir visualmente |
| RFim-1.5 | O botão "Cadastrar Novo Cliente" está visível e não quebra a página ao ser clicado | Clicar; nada deve acontecer e nenhum erro deve surgir no console |
| RFim-1.6 | O fundo é branco e os destaques são azuis | Conferir visualmente |
| RFim-1.7 | Nenhum erro no console do navegador nem no terminal do servidor | Abrir o console (F12) e olhar o terminal |

---

**Etapa anterior:** [00 — Ambiente](00-ambiente.md) ·
**Próxima etapa:** [02 — Cadastro de clientes](02-cadastro-de-clientes.md)
