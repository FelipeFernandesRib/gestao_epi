from django.db import models
from colaboradores.models import Colaborador
from epis.models import Epi

# Create your models here.
class Emprestimo(models.Model):
    STATUS_CHOICES = [
        ('EMPRESTADO', 'Emprestado'),
        ('DEVOLVIDO', 'Devolvido'),
        ('PERDIDO', 'Perdido'),
    ]

    colaborador = models.ForeignKey(Colaborador, on_delete=models.CASCADE)
    epi = models.ForeignKey(Epi, on_delete=models.CASCADE)
    data_emprestimo = models.DateTimeField(auto_now_add=True)
    data_devolucao = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='EMPRESTADO')

    def __str__(self):
        return f"{self.colaborador.nome} - {self.epi.nome} ({self.status})"