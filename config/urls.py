"""Rotas principais do projeto.

Cada app do projeto deve expor o seu próprio `urls.py` e ser incluído aqui.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
]

# Em desenvolvimento, o Django serve os arquivos de mídia enviados por usuários.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
