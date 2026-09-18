# Etapa 3 — Busca automática por CNPJ

> **Objetivo:** permitir que o usuário informe um CNPJ e o sistema preencha
> sozinho os campos do cadastro, consultando a API pública da **ReceitaWS**.

Documentação da API:
<https://developers.receitaws.com.br/#/operations/queryRFFree>

---

## Requisitos de início

| # | Requisito | Como verificar |
| --- | --- | --- |
| RI-3.1 | [Etapa 2](02-cadastro-de-clientes.md) concluída | Todos os critérios `RFim-2.x` atendidos |
| RI-3.2 | Tela `/clientes/novo/` funcionando com cadastro manual | Cadastrar um cliente à mão |
| RI-3.3 | Campo `cnpj` presente no modelo `Cliente` | Conferir `core/models.py` |
| RI-3.4 | Máquina com acesso à internet | Abrir <https://receitaws.com.br> no navegador |

---

## A API da ReceitaWS

**Endpoint gratuito (sem token):**

```
GET https://receitaws.com.br/v1/cnpj/{cnpj}
```

`{cnpj}` são os **14 dígitos**, sem pontuação.

A resposta é um JSON. Os campos que nos interessam:

| Campo da API | Campo do `Cliente` | Observação |
| --- | --- | --- |
| `status` | — | `"OK"` ou `"ERROR"` |
| `message` | — | Mensagem de erro, quando `status = "ERROR"` |
| `nome` | `nome` | Razão social |
| `cnpj` | `cnpj` | Já vem formatado |
| `porte` | `porte` | `MICRO EMPRESA`, `EMPRESA DE PEQUENO PORTE`, `DEMAIS` |
| `abertura` | `abertura` | Formato `dd/mm/aaaa` |
| `logradouro` | `rua` | |
| `numero` | `numero` | |
| `municipio` | `cidade` | |
| `uf` | `estado` | |
| `cep` | `cep` | Costuma vir como `00.000-000` |

> **Atenção — limite do plano gratuito.** A API livre aceita poucas consultas
> por minuto (na ordem de 3). Ao estourar o limite, ela responde com o código
> HTTP **429**. Em sala, combine de não ficar repetindo a mesma busca.

> **Leitura defensiva.** Nem todo CNPJ devolve todos os campos. O código lê cada
> campo com um valor padrão vazio (`dados.get("porte", "")`) e nunca assume que
> a chave existe.

---

## Requisitos funcionais

### RF-3.1 — A consulta passa pelo servidor Django

O navegador **não** chama a ReceitaWS diretamente: ele chama o nosso servidor,
que por sua vez chama a API e devolve o resultado.

```
Navegador  ──fetch──▶  Django (/api/cnpj/<cnpj>/)  ──HTTP──▶  ReceitaWS
```

Três motivos para esse desvio:

1. **CORS** — o navegador bloqueia requisições de `localhost:8000` para outro
   domínio que não autorize a origem explicitamente.
2. **Controle de erros** — o Django traduz falhas de rede, tempo esgotado e
   limite de uso em respostas previsíveis para a tela.
3. **Evolução** — se um dia a API passar a exigir token, ele fica no servidor,
   e não exposto no JavaScript.

### RF-3.2 — Endpoint interno de consulta

Nova rota `/api/cnpj/<cnpj>/` (nome: `core:consulta_cnpj`), que:

1. Mantém apenas os dígitos do CNPJ recebido e valida que sobraram 14.
2. Chama a ReceitaWS com **tempo limite de 10 segundos**.
3. Devolve um `JsonResponse` no formato abaixo.

**Sucesso (HTTP 200)**

```json
{
  "ok": true,
  "cliente": {
    "nome": "EMPRESA MANEIRA LTDA",
    "cnpj": "00.000.000/0001-00",
    "porte": "DEMAIS",
    "abertura": "2005-11-08",
    "rua": "AVENIDA BRASIL",
    "numero": "1500",
    "cidade": "PORTO ALEGRE",
    "estado": "RS",
    "cep": "90000-000"
  }
}
```

**Erro (HTTP 400, 429, 502 ou 504)**

```json
{ "ok": false, "erro": "CNPJ não encontrado." }
```

### RF-3.3 — Tratamento de erros

| Situação | Status devolvido | Mensagem exibida ao usuário |
| --- | --- | --- |
| CNPJ sem 14 dígitos | 400 | "Informe um CNPJ com 14 dígitos." |
| API respondeu `status: "ERROR"` | 400 | A `message` devolvida pela API |
| Limite de consultas estourado (429) | 429 | "Muitas consultas seguidas. Aguarde um minuto e tente de novo." |
| Tempo limite esgotado | 504 | "A consulta demorou demais. Tente novamente." |
| Qualquer outra falha de rede | 502 | "Não foi possível consultar a Receita agora." |

Nenhuma dessas situações derruba a página: o usuário continua podendo preencher
o formulário manualmente.

### RF-3.4 — Conversões antes de devolver

| Campo | Conversão |
| --- | --- |
| `abertura` | `dd/mm/aaaa` → `aaaa-mm-dd`, formato aceito pelo `<input type="date">` |
| `cep` | Só os dígitos, depois a máscara `00000-000` |
| `estado` | Maiúsculas |
| `porte` | Se vier um valor fora da lista de `choices`, devolver vazio |

### RF-3.5 — Botão "Buscar por CNPJ"

Na tela `/clientes/novo/`, acima do formulário, um botão **Buscar por CNPJ**.
Ao ser clicado, abre um popup (modal).

### RF-3.6 — Popup de busca

O modal contém:

- Título: `Buscar por CNPJ`
- Um campo de texto para o CNPJ, com foco automático ao abrir
- Um botão **Buscar** (ação primária) e um botão **Cancelar**
- Uma área de mensagem, onde aparecem o estado "Consultando…" e os erros

**Comportamentos**

- Enquanto a consulta acontece, o botão Buscar fica desabilitado e exibe
  "Consultando…" — evita disparar duas chamadas.
- Consulta bem-sucedida: o modal fecha e os campos do formulário são
  preenchidos com os dados recebidos.
- Consulta com erro: o modal **continua aberto**, exibindo a mensagem, para que
  o usuário corrija o CNPJ.
- O modal fecha com o botão Cancelar, com a tecla `Esc` ou com um clique fora
  da caixa.

### RF-3.7 — Os dados preenchidos continuam editáveis

O preenchimento automático é um atalho, não uma trava: todos os campos seguem
editáveis, e o cadastro só é gravado quando o usuário clica em **Salvar**. A
gravação continua sendo a da [Etapa 2](02-cadastro-de-clientes.md) — a busca por
CNPJ não grava nada sozinha.

---

## Arquivos envolvidos

| Arquivo | O que muda |
| --- | --- |
| `core/services.py` | **Novo** — função que chama a ReceitaWS e converte a resposta |
| `core/views.py` | Nova view `consulta_cnpj` |
| `core/urls.py` | Rota `api/cnpj/<str:cnpj>/` |
| `templates/core/cliente_form.html` | Botão "Buscar por CNPJ" e a marcação do modal |
| `static/js/main.js` | Abertura/fechamento do modal, `fetch` e preenchimento dos campos |
| `static/css/styles.css` | Estilos de modal (sobreposição, caixa central, botões) |

> A chamada HTTP usa `urllib.request`, da biblioteca padrão do Python — assim
> não acrescentamos dependência ao `requirements.txt`.

---

## Requisitos de fim

| # | Critério de aceite | Como verificar |
| --- | --- | --- |
| RFim-3.1 | O botão "Buscar por CNPJ" aparece na tela de cadastro | Abrir `/clientes/novo/` |
| RFim-3.2 | O botão abre o modal com campo de CNPJ | Clicar no botão |
| RFim-3.3 | Um CNPJ válido preenche nome, porte, abertura e endereço | Buscar um CNPJ real e conferir os campos |
| RFim-3.4 | Após a busca bem-sucedida, o modal fecha sozinho | Conferir visualmente |
| RFim-3.5 | Um CNPJ inválido mostra mensagem de erro e mantém o modal aberto | Buscar `00000000000000` |
| RFim-3.6 | Sem internet, a tela exibe erro e não trava | Desligar a rede e buscar |
| RFim-3.7 | O cliente preenchido automaticamente é gravado ao clicar em Salvar | Salvar e conferir a tela principal |
| RFim-3.8 | Os campos preenchidos podem ser editados antes de salvar | Alterar o nome e salvar |
| RFim-3.9 | O modal fecha com `Esc`, com Cancelar e com clique fora | Testar os três caminhos |

---

**Etapa anterior:** [02 — Cadastro de clientes](02-cadastro-de-clientes.md) ·
**Próxima etapa:** [04 — Tela do cliente](04-tela-do-cliente.md)
