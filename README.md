# Sistemas de Informação Aplicados ao Empreendedorismo

> **Utilizando o conhecimento do curso no Mercado de Trabalho**
> Minicurso de extensão — Bacharelado em Sistemas de Informação · IFRS

Este repositório é o **ambiente base** do exercício prático do minicurso. Ele já
vem com um projeto Django funcionando (HTML, CSS e JavaScript), uma tela inicial
e a pasta [`docs/`](docs/), onde ficarão as especificações do sistema.

A partir dele, desenvolveremos juntos uma pequena plataforma Web usando
**SDD — Spec Driven Development**: escrevemos primeiro a especificação, em
Markdown, e só então o código que a implementa.

---

## Sumário

- [Pré-requisitos](#pré-requisitos)
- [Como rodar o projeto](#como-rodar-o-projeto)
- [Estrutura do repositório](#estrutura-do-repositório)
- [Comandos úteis](#comandos-úteis)
- [Como trabalharemos com SDD](#como-trabalharemos-com-sdd)
- [Onde escrever cada tipo de código](#onde-escrever-cada-tipo-de-código)
- [Problemas comuns](#problemas-comuns)

---

## Pré-requisitos

| Ferramenta | Versão | Observação |
| --- | --- | --- |
| [Python](https://www.python.org/downloads/) | 3.10 ou superior | Exigido pelo Django 5.2 |
| [Git](https://git-scm.com/downloads) | qualquer versão recente | Para clonar o repositório |
| Editor de código | — | Recomendado: [VS Code](https://code.visualstudio.com/) |

Confira sua versão do Python antes de começar:

```bash
python3 --version   # macOS / Linux
python --version    # Windows
```

> Não é necessário instalar banco de dados: o projeto usa **SQLite**, que já vem
> junto com o Python.

---

## Como rodar o projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/minellera/minicurso-bsi-aplicado.git
cd minicurso-bsi-aplicado
```

### 2. Criar e ativar o ambiente virtual

O ambiente virtual (`.venv`) isola as dependências deste projeto das demais
instaladas na sua máquina.

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell)**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Windows (Prompt de Comando)**

```cmd
python -m venv .venv
.\.venv\Scripts\activate.bat
```

Com o ambiente ativo, o nome `(.venv)` aparece no início da linha do terminal.
Para sair dele, use `deactivate`.

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Criar o arquivo de variáveis de ambiente

```bash
cp .env.example .env      # macOS / Linux
copy .env.example .env    # Windows
```

O projeto funciona sem o `.env` (há valores padrão para desenvolvimento), mas
criá-lo é a prática correta e evita surpresas mais adiante.

### 5. Preparar o banco de dados

```bash
python manage.py migrate
```

### 6. Rodar o servidor

```bash
python manage.py runserver
```

Abra <http://127.0.0.1:8000/> no navegador. Você deve ver a tela inicial com o
nome do minicurso. Para parar o servidor, pressione `Ctrl + C`.

### 7. (Opcional) Criar um usuário administrador

Dá acesso ao painel do Django em <http://127.0.0.1:8000/admin/>:

```bash
python manage.py createsuperuser
```

---

## Estrutura do repositório

```
minicurso-bsi-aplicado/
├── config/              # Configuração do projeto Django
│   ├── settings.py      # Configurações (apps, banco, templates, estáticos)
│   ├── urls.py          # Rotas principais do projeto
│   ├── wsgi.py          # Entrada para servidores WSGI
│   └── asgi.py          # Entrada para servidores ASGI
├── core/                # App principal da aplicação
│   ├── models.py        # Modelos (tabelas do banco de dados)
│   ├── views.py         # Views (lógica que responde às requisições)
│   ├── urls.py          # Rotas do app
│   ├── admin.py         # Registro de modelos no painel admin
│   └── tests.py         # Testes automatizados
├── templates/           # Templates HTML
│   ├── base.html        # Layout compartilhado por todas as telas
│   └── core/
│       └── index.html   # Tela inicial
├── static/              # Arquivos estáticos servidos ao navegador
│   ├── css/styles.css   # Estilos globais
│   ├── js/main.js       # JavaScript global
│   └── img/             # Imagens
├── docs/                # Specs em Markdown (SDD) — ver docs/README.md
├── manage.py            # Utilitário de linha de comando do Django
├── requirements.txt     # Dependências do projeto
└── .env.example         # Modelo de variáveis de ambiente
```

---

## Comandos úteis

Todos os comandos abaixo pressupõem o ambiente virtual **ativado**.

| Comando | O que faz |
| --- | --- |
| `python manage.py runserver` | Sobe o servidor de desenvolvimento |
| `python manage.py runserver 8080` | Sobe o servidor em outra porta |
| `python manage.py makemigrations` | Gera migrações a partir das mudanças nos modelos |
| `python manage.py migrate` | Aplica as migrações no banco de dados |
| `python manage.py createsuperuser` | Cria um usuário administrador |
| `python manage.py test` | Executa os testes automatizados |
| `python manage.py shell` | Abre um terminal Python com o Django carregado |
| `python manage.py check` | Verifica se há problemas de configuração |

---

## Como trabalharemos com SDD

**Spec Driven Development** inverte a ordem habitual: a especificação vem antes
do código e permanece como fonte da verdade durante todo o desenvolvimento.

O ciclo que seguiremos no minicurso:

1. **Entender o problema** — a definição do problema será publicada em `docs/`.
2. **Escrever a spec** — requisitos, modelo de dados e telas, em Markdown.
3. **Revisar a spec** — ambiguidades resolvidas aqui custam muito menos do que
   depois, no código.
4. **Implementar** — cada trecho de código atende a um requisito identificado
   (`RF-01`, `RF-02`, …).
5. **Validar** — conferir o resultado contra os critérios de aceite da spec.
6. **Evoluir** — mudou o escopo? A spec muda primeiro; o código vem depois.

As especificações ficarão em [`docs/`](docs/). Leia o
[guia daquela pasta](docs/README.md) para conhecer a organização dos arquivos.

---

## Onde escrever cada tipo de código

| Quero… | Mexo em… |
| --- | --- |
| Criar uma nova tela | `core/views.py` + `core/urls.py` + `templates/core/` |
| Alterar o layout comum a todas as telas | `templates/base.html` |
| Mudar cores, espaçamentos, tipografia | `static/css/styles.css` |
| Adicionar interatividade no navegador | `static/js/main.js` |
| Criar ou alterar tabelas do banco | `core/models.py` (depois `makemigrations` e `migrate`) |
| Registrar um modelo no painel admin | `core/admin.py` |
| Escrever testes automatizados | `core/tests.py` |

> **Arquivos estáticos:** sempre referencie CSS, JS e imagens com a tag
> `{% static %}` nos templates — nunca com caminhos fixos como `/static/...`.

---

## Problemas comuns

**`python: command not found`**
Use `python3` no lugar de `python` (macOS e Linux) ou reinstale o Python no
Windows marcando a opção *Add Python to PATH*.

**`ModuleNotFoundError: No module named 'django'`**
O ambiente virtual não está ativado ou as dependências não foram instaladas.
Ative o `.venv` e rode `pip install -r requirements.txt` novamente.

**`Error: That port is already in use.`**
Já existe um servidor rodando. Feche-o com `Ctrl + C` ou use outra porta:
`python manage.py runserver 8080`.

**A execução de scripts está desabilitada (PowerShell)**
Libere a execução para o usuário atual e ative o ambiente novamente:
`Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`.

**Alterei o CSS/JS e nada mudou no navegador**
É cache. Recarregue a página forçando a atualização: `Ctrl + F5` (Windows/Linux)
ou `Cmd + Shift + R` (macOS).

---

## Créditos

Material desenvolvido para o minicurso de extensão do curso de Bacharelado em
Sistemas de Informação do **IFRS**.
