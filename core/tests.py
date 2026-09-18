"""Testes do app `core`.

Execute com: python manage.py test
"""

from django.test import TestCase
from django.urls import reverse


class IndexViewTests(TestCase):
    def test_index_responde_200(self):
        resposta = self.client.get(reverse("core:index"))
        self.assertEqual(resposta.status_code, 200)

    def test_index_exibe_titulo_do_minicurso(self):
        resposta = self.client.get(reverse("core:index"))
        self.assertContains(
            resposta,
            "Sistemas de Informação Aplicados ao Empreendedorismo",
        )
