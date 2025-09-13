from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_emprestimos, name='lista_emprestimos'),
    path('novo/', views.criar_emprestimo, name='criar_emprestimo'),
    path('editar/<int:id>/', views.editar_emprestimo, name='editar_emprestimo'),
    path('devolver/<int:pk>/', views.devolver_emprestimo, name='devolver_emprestimo'),
    path('<int:pk>/perdido/', views.marcar_perdido, name='marcar_perdido'),
     path('relatorios/', views.relatorios_emprestimos, name='relatorios_emprestimos'),
]