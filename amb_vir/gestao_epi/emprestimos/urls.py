from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_emprestimos, name='lista_emprestimos'),
    path('novo/', views.criar_emprestimo, name='criar_emprestimo'),
    path('editar/<int:id>/', views.editar_emprestimo, name='editar_emprestimo'),
    path('excluir/<int:id>/', views.excluir_emprestimo, name='excluir_emprestimo'),

    
]