from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('cadastros/', include('cadastros.urls')),
    
    # URLs de Autenticação padrão do Django
    path('usuarios/', include('django.contrib.auth.urls')),
]

# Configurações para ambiente de desenvolvimento (DEBUG = True)
if settings.DEBUG:
    # 1. Suporte a arquivos de mídia (fotos enviadas)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    # 2. Registra as URLs do Django Debug Toolbar (Corrige o erro 'djdt')
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]