# Etapa 0 — Ambiente configurado

> **Objetivo:** garantir que qualquer pessoa da turma consiga rodar a aplicação
> na própria máquina, em `http://localhost:8000/`, antes de escrevermos
> qualquer funcionalidade do sistema.

Nesta etapa **não escrevemos código de produto**. Só confirmamos que o ambiente
base (Django + HTML + CSS + JavaScript) está instalado e funcionando.

---

## Requisitos de início

| # | Requisito | Como verificar |
| --- | --- | --- |
| RI-0.1 | Python 3.10 ou superior instalado | `python3 --version` |
| RI-0.2 | Git instalado | `git --version` |
| RI-0.3 | Repositório clonado na máquina | `ls manage.py` retorna o arquivo |
| RI-0.4 | Editor de código instalado | Abrir a pasta do projeto no VS Code |

> Não é necessário instalar banco de dados: o projeto usa **SQLite**, que já vem
> junto com o Python.

---

## Requisitos funcionais

### RF-0.1 — Ambiente virtual isolado

As dependências do projeto ficam em um ambiente virtual (`.venv`) na raiz do
repositório, e não instaladas globalmente na máquina.

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

Com o ambiente ativo, o prefixo `(.venv)` aparece no início da linha do terminal.

### RF-0.2 — Dependências instaladas

```bash
pip install -r requirements.txt
```

O arquivo `requirements.txt` declara as dependências do ambiente base:

| Pacote | Versão | Para que serve |
| --- | --- | --- |
| `Django` | 5.2.17 | Framework web que responde às requisições |
| `python-dotenv` | 1.2.3 | Lê as variáveis do arquivo `.env` |

### RF-0.3 — Variáveis de ambiente

```bash
cp .env.example .env      # macOS / Linux
copy .env.example .env    # Windows
```

O projeto funciona sem o `.env` (há valores padrão para desenvolvimento), mas
criá-lo é a prática correta: é nele que ficam a `SECRET_KEY` e o modo `DEBUG`.
O `.env` **não** é versionado (já consta no `.gitignore`).

### RF-0.4 — Banco de dados preparado

```bash
python manage.py migrate
```

Cria o arquivo `db.sqlite3` com as tabelas internas do Django (usuários,
sessões, admin). Ainda não há tabelas do nosso sistema — elas surgem na
[Etapa 2](02-cadastro-de-clientes.md).

### RF-0.5 — Servidor rodando na porta 8000

O comando que encerra esta etapa:

```bash
python manage.py runserver 8000
```

A aplicação fica disponível em <http://localhost:8000/>. Para parar o servidor,
pressione `Ctrl + C`.

> `python manage.py runserver` (sem argumento) já usa a porta 8000 por padrão.
> Escrevemos a porta de forma explícita para deixar o resultado esperado claro.

### RF-0.6 — (Opcional) Usuário administrador

```bash
python manage.py createsuperuser
```

Dá acesso ao painel do Django em <http://localhost:8000/admin/>, útil para
conferir os dados gravados nas etapas seguintes.

---

## Requisitos de fim

Esta etapa só está concluída quando **todos** os itens abaixo forem verdadeiros:

| # | Critério de aceite | Como verificar |
| --- | --- | --- |
| RFim-0.1 | O comando `python manage.py check` termina sem erros | Nenhuma mensagem de `ERRORS` no terminal |
| RFim-0.2 | O servidor sobe sem exceções | `python manage.py runserver 8000` exibe `Starting development server at http://127.0.0.1:8000/` |
| RFim-0.3 | A página inicial abre no navegador | <http://localhost:8000/> carrega a tela do minicurso |
| RFim-0.4 | O CSS está sendo servido | A página aparece estilizada, não como texto puro |
| RFim-0.5 | O JavaScript está sendo servido | O console do navegador exibe `[minicurso] Ambiente base carregado…` |
| RFim-0.6 | O banco foi criado | O arquivo `db.sqlite3` existe na raiz do projeto |

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

---

**Próxima etapa:** [01 — Tela principal](01-tela-principal.md)
