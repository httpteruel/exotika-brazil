from django.urls import path
from .views import EspecieList, EspecieCreate, EspecieUpdate, EspecieDelete

urlpatterns = [

    path('especies/', EspecieList.as_view(), name='listar-especie'),
    path('especies/cadastrar/', EspecieCreate.as_view(), name='cadastrar-especie'),
    path('especies/editar/<int:pk>/', EspecieUpdate.as_view(), name='editar-especie'),
    path('especies/excluir/<int:pk>/', EspecieDelete.as_view(), name='excluir-especie'),
]