from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_colaboradores, name='lista_colaboradores'),
    path('novo/', views.criar_colaborador, name='criar_colaborador'),
    path('editar/<int:id>/', views.editar_colaborador, name='editar_colaborador'),
    path('excluir/<int:id>/', views.excluir_colaborador, name='excluir_colaborador'),
]