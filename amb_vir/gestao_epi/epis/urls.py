from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_epis, name='lista_epis'), 
    path('criar/', views.criar_epi, name='criar_epi'),
    path('editar/<int:pk>/', views.editar_epi, name='editar_epi'),
    path('excluir/<int:pk>/', views.excluir_epi, name='excluir_epi'),
]
