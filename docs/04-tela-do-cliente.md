# Etapa 4 — Tela do cliente

> **Objetivo:** criar a tela de detalhe de um cliente, com edição dos dados, o
> espaço reservado para os documentos e a exclusão do cliente com confirmação.

---

## Requisitos de início

| # | Requisito | Como verificar |
| --- | --- | --- |
| RI-4.1 | [Etapa 3](03-busca-por-cnpj.md) concluída | Todos os critérios `RFim-3.x` atendidos |
| RI-4.2 | Pelo menos um cliente cadastrado | A tela principal mostra a lista preenchida |
| RI-4.3 | `ClienteForm` funcionando | O cadastro grava e valida corretamente |

---

## Rotas desta etapa

| Rota | Nome | Método | Função |
| --- | --- | --- | --- |
| `/clientes/<int:pk>/` | `core:cliente_detalhe` | GET | Tela do cliente |
| `/clientes/<int:pk>/editar/` | `core:cliente_editar` | GET, POST | Edição dos dados |
| `/clientes/<int:pk>/excluir/` | `core:cliente_excluir` | POST | Exclusão |

Um `pk` inexistente responde **404** (usar `get_object_or_404`).

---

## Requisitos funcionais

### RF-4.1 — O cliente vira link na tela principal

Cada cliente listado na tela principal é clicável e leva para
`/clientes/<pk>/`. A área clicável é o card/linha inteiro, não apenas o nome.

### RF-4.2 — Cabeçalho do cliente

No topo da tela de detalhe, um bloco com **todas** as informações do cliente:

- Nome (como título da tela)
- CNPJ
- Porte
- Data de abertura (formatada como `dd/mm/aaaa`)
- Endereço completo: rua, número, cidade, estado e CEP

Campos vazios aparecem com um traço (`—`) em vez de sumirem, para que a
ausência do dado seja visível.

### RF-4.3 — Botão Editar

No **canto superior direito** do bloco de cabeçalho, um botão **Editar**, que
leva para `/clientes/<pk>/editar/`.

### RF-4.4 — Tela de edição

Reutiliza o mesmo `ClienteForm` e o mesmo template da
[Etapa 2](02-cadastro-de-clientes.md), agora preenchido com os dados atuais
(`ClienteForm(instance=cliente)`).

- Título da tela: `Editar cliente`
- Salvar → grava as alterações e redireciona para a **tela do cliente**
- Cancelar → volta para a tela do cliente sem gravar
- O botão "Buscar por CNPJ" continua disponível também na edição

> **Decisão D-4.1 — um único template para cadastro e edição.** O formulário é o
> mesmo; muda apenas o título, o destino do POST e o destino do Cancelar. Manter
> dois templates quase idênticos dobraria o trabalho de qualquer ajuste futuro.

### RF-4.5 — Seção de documentos (reservada)

Abaixo do cabeçalho, uma seção intitulada **Documentos**, por enquanto com um
estado vazio: *"Nenhum documento enviado ainda."*

A seção é preenchida na [Etapa 5](05-envio-de-documentos.md). Criá-la agora
deixa a estrutura da tela pronta e evita retrabalho de layout.

### RF-4.6 — Excluir cliente

No **final da tela**, separado do restante do conteúdo, um botão **Excluir
Cliente**, com aparência de ação destrutiva (vermelho ou contorno vermelho).

### RF-4.7 — Confirmação antes de excluir

A exclusão **nunca** acontece em um único clique.

- Clicar em "Excluir Cliente" abre um modal de confirmação.
- O modal exibe o nome do cliente e um aviso de que a ação não pode ser
  desfeita.
- O modal tem dois botões: **Cancelar** (fecha e não faz nada) e **Excluir**
  (confirma).
- Só a confirmação dispara o `POST` para `/clientes/<pk>/excluir/`, com
  `{% csrf_token %}`.
- Após excluir, o usuário é redirecionado para a tela principal, onde o cliente
  não aparece mais.

> **Por que `POST` e não `GET`.** Um link `GET` que apaga dados pode ser
> disparado por um pré-carregamento do navegador ou por um robô de indexação.
> Ações que alteram o estado do sistema vão por `POST`.

---

## Arquivos envolvidos

| Arquivo | O que muda |
| --- | --- |
| `core/urls.py` | Três novas rotas |
| `core/views.py` | Views `cliente_detalhe`, `cliente_editar`, `cliente_excluir` |
| `templates/core/index.html` | Cada cliente vira link para o detalhe |
| `templates/core/cliente_detalhe.html` | **Novo** — cabeçalho, seção de documentos e exclusão |
| `templates/core/cliente_form.html` | Passa a servir cadastro **e** edição |
| `static/js/main.js` | Modal de confirmação de exclusão |
| `static/css/styles.css` | Estilos do cabeçalho, da lista de dados e do botão destrutivo |

---

## Requisitos de fim

| # | Critério de aceite | Como verificar |
| --- | --- | --- |
| RFim-4.1 | Clicar em um cliente na tela principal abre `/clientes/<pk>/` | Clicar e conferir a URL |
| RFim-4.2 | O cabeçalho exibe todos os campos do cliente | Conferir com os dados cadastrados |
| RFim-4.3 | Campos vazios aparecem como `—` | Cadastrar um cliente só com nome e abrir |
| RFim-4.4 | O botão Editar está no canto superior direito do cabeçalho | Conferir visualmente |
| RFim-4.5 | A edição carrega os dados atuais e salva as alterações | Trocar a cidade e salvar |
| RFim-4.6 | Após salvar a edição, volta para a tela do cliente já atualizada | Conferir visualmente |
| RFim-4.7 | A seção Documentos aparece com o estado vazio | Conferir visualmente |
| RFim-4.8 | O botão "Excluir Cliente" está no final da tela | Rolar até o fim |
| RFim-4.9 | A exclusão exige confirmação | Clicar em Excluir e cancelar: o cliente continua existindo |
| RFim-4.10 | Confirmar a exclusão remove o cliente e volta para a tela principal | Excluir um cliente de teste |
| RFim-4.11 | Um `pk` inexistente devolve 404 | Abrir `/clientes/9999/` |

---

**Etapa anterior:** [03 — Busca por CNPJ](03-busca-por-cnpj.md) ·
**Próxima etapa:** [05 — Envio de documentos](05-envio-de-documentos.md)
