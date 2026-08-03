from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Importa a IndexView dinamicamente do app cadastros
from cadastros.views import IndexView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('cadastros/', include('cadastros.urls')),
    
    path('usuarios/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    # 1. Suporte a arquivos de mídia (fotos enviadas)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    # 2. Registra as URLs do Django Debug Toolbar
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]