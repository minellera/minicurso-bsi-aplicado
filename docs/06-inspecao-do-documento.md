# Etapa 6 — Inspeção do documento

> **Objetivo:** ao clicar no card de um documento, abrir um popup com o nome, a
> descrição e a pré-visualização completa do documento, além das ações de
> **Download**, **Editar** e **Excluir**.

---

## Requisitos de início

| # | Requisito | Como verificar |
| --- | --- | --- |
| RI-6.1 | [Etapa 5](05-envio-de-documentos.md) concluída | Todos os critérios `RFim-5.x` atendidos |
| RI-6.2 | Documentos dos três tipos cadastrados | Ter um PNG/JPG, um PDF e uma URL em um cliente |
| RI-6.3 | Arquivos sendo servidos em `/media/` | Abrir a URL de um arquivo direto no navegador |
| RI-6.4 | Propriedade `tipo` do `Documento` funcionando | Conferir no `python manage.py shell` |

---

## Rotas desta etapa

| Rota | Nome | Método | Função |
| --- | --- | --- | --- |
| `/documentos/<int:pk>/download/` | `core:documento_download` | GET | Baixa o arquivo |
| `/documentos/<int:pk>/editar/` | `core:documento_editar` | POST | Salva nome e descrição |
| `/documentos/<int:pk>/excluir/` | `core:documento_excluir` | POST | Exclui o documento |

Todas redirecionam para a tela do cliente correspondente
(`documento.cliente.pk`) ao final.

---

## Requisitos funcionais

### RF-6.1 — O card abre o popup

Clicar em qualquer ponto do card abre o popup de inspeção daquele documento.
O card recebe indicação visual de ser clicável (cursor de mão e realce no
`hover`), e responde também ao teclado — `Tab` para focar, `Enter` para abrir.

### RF-6.2 — Conteúdo do popup

| Área | Conteúdo |
| --- | --- |
| Topo à esquerda | Nome do documento |
| Topo à direita | Botões **Download**, **Editar** e **Excluir** |
| Abaixo do topo | Descrição (ou "Sem descrição") |
| Corpo | Pré-visualização do documento |
| Rodapé | Tipo, tamanho e data de envio |

O popup é maior que os anteriores — a pré-visualização precisa de espaço. Ele
ocupa até 900px de largura e até 90% da altura da janela, com rolagem interna
quando o conteúdo passar disso.

### RF-6.3 — Pré-visualização por tipo

| Tipo | Como é exibido |
| --- | --- |
| PNG / JPG | `<img>` com a imagem inteira, ajustada à largura do popup |
| PDF | `<iframe>` (ou `<embed>`) com o PDF completo, navegável por páginas, com altura mínima de 500px |
| URL | O endereço em destaque, como link que abre em nova aba (`target="_blank"` com `rel="noopener"`) |

> **Decisão D-6.1 — URL não vira `iframe`.** A maioria dos sites envia o
> cabeçalho `X-Frame-Options`, que impede a exibição dentro de um quadro: o
> resultado seria uma área em branco. Um link explícito é honesto sobre o que o
> sistema consegue mostrar.

### RF-6.4 — Download

O botão **Download** entrega o arquivo com o nome original preservado
(`FileResponse` com `as_attachment=True`).

Para documentos do tipo URL, o botão é substituído por **Abrir link**, que
aponta para o endereço cadastrado — não há arquivo nosso para baixar.

### RF-6.5 — Editar

O botão **Editar** troca, dentro do mesmo popup, a área de descrição por um
formulário com:

- Campo de **Nome** (obrigatório)
- Campo de **Descrição**
- Botões **Salvar** e **Cancelar**

Comportamentos:

- **Cancelar** volta à visualização, sem gravar, com os valores originais.
- **Salvar** envia `POST` para `/documentos/<pk>/editar/` e recarrega a tela do
  cliente com os dados atualizados.
- O **arquivo em si não é substituído** nesta etapa: editam-se apenas nome e
  descrição. Para trocar o arquivo, exclui-se o documento e envia-se outro.

> **Decisão D-6.2 — por que o arquivo não é editável.** Trocar o arquivo
> significaria apagar o anterior do disco, revalidar extensão e tamanho e
> recalcular o campo `tamanho`. É um fluxo próprio, e o escopo desta etapa pede
> edição de metadados.

### RF-6.6 — Excluir com confirmação

- Clicar em **Excluir** exibe uma confirmação dentro do próprio popup: uma
  pergunta clara ("Excluir o documento *Nome*? Esta ação não pode ser
  desfeita.") e dois botões, **Cancelar** e **Excluir**.
- **Cancelar** volta ao estado normal do popup, e nada é excluído.
- A confirmação dispara `POST` para `/documentos/<pk>/excluir/`.
- Excluído o documento, o popup fecha e a tela do cliente é recarregada sem o
  card correspondente.
- O arquivo também é removido do disco (`documento.arquivo.delete()`).

### RF-6.7 — Fechar o popup

O popup fecha pelo botão de fechar (`×`), pela tecla `Esc` ou por clique fora da
caixa. Fechar durante uma edição descarta as alterações não salvas.

---

## Arquivos envolvidos

| Arquivo | O que muda |
| --- | --- |
| `core/urls.py` | Três novas rotas de documento |
| `core/views.py` | Views `documento_download`, `documento_editar`, `documento_excluir` |
| `templates/core/cliente_detalhe.html` | Cards clicáveis e a marcação do popup de inspeção |
| `static/js/main.js` | Abertura do popup com os dados do card, alternância entre ver/editar/confirmar |
| `static/css/styles.css` | Estilos do popup grande, da pré-visualização e da barra de ações |

> Os dados de cada documento chegam ao JavaScript por atributos `data-*` no
> próprio card (`data-nome`, `data-descricao`, `data-tipo`, `data-src`, …).
> Assim a tela do cliente continua com uma única requisição, sem precisar de um
> endpoint extra para buscar o documento.

---

## Requisitos de fim

| # | Critério de aceite | Como verificar |
| --- | --- | --- |
| RFim-6.1 | Clicar no card abre o popup de inspeção | Clicar em qualquer card |
| RFim-6.2 | O popup exibe nome e descrição | Conferir com os dados cadastrados |
| RFim-6.3 | Documento sem descrição exibe "Sem descrição" | Enviar um documento sem descrição |
| RFim-6.4 | Imagem é exibida por inteiro | Abrir um PNG e um JPG |
| RFim-6.5 | PDF é exibido e permite navegar entre as páginas | Abrir um PDF de várias páginas |
| RFim-6.6 | Documento do tipo URL mostra o link, que abre em nova aba | Abrir um documento de URL |
| RFim-6.7 | Os três botões estão no canto superior direito do popup | Conferir visualmente |
| RFim-6.8 | Download baixa o arquivo com o nome original | Clicar em Download |
| RFim-6.9 | Editar permite alterar nome e descrição e salvar | Renomear um documento |
| RFim-6.10 | Cancelar a edição descarta as alterações | Alterar o nome e cancelar |
| RFim-6.11 | Excluir exige confirmação | Clicar em Excluir e cancelar: o documento continua lá |
| RFim-6.12 | Confirmar a exclusão remove o card e o arquivo do disco | Excluir e conferir a pasta `media/` |
| RFim-6.13 | O popup fecha com `Esc`, com `×` e com clique fora | Testar os três caminhos |

---

**Etapa anterior:** [05 — Envio de documentos](05-envio-de-documentos.md) ·
**Próxima etapa:** [07 — Pesquisa de documentos](07-pesquisa-de-documentos.md)
