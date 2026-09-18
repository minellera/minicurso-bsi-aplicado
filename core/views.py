"""Views do app `core`."""

from django.shortcuts import render

MINICURSO = {
    "titulo": "Sistemas de Informação Aplicados ao Empreendedorismo",
    "subtitulo": "Utilizando o conhecimento do curso no Mercado de Trabalho",
    "instituicao": "IFRS — Bacharelado em Sistemas de Informação",
}


def index(request):
    """Página inicial do projeto base do minicurso."""
    return render(request, "core/index.html", {"minicurso": MINICURSO})
