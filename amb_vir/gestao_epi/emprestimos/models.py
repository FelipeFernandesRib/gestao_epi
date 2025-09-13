from django.db import models
from django.utils import timezone
from colaboradores.models import Colaborador
from epis.models import Epi

class Emprestimo(models.Model):
    STATUS_CHOICES = [
        ('EMPRESTADO', 'Emprestado'),
        ('DEVOLVIDO', 'Devolvido'),
        ('PERDIDO', 'Perdido'),
    ]

    colaborador = models.ForeignKey('colaboradores.Colaborador', on_delete=models.CASCADE)
    epi = models.ForeignKey('epis.Epi', on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)
    data_emprestimo = models.DateTimeField(auto_now_add=True)
    data_devolucao = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='EMPRESTADO')

    def devolver(self):
        if self.status == "EMPRESTADO":
            self.status = "DEVOLVIDO"
            self.data_devolucao = timezone.now()
            self.save()
             
            pass 
    
    def is_em_andamento(self):
        return self.status == "EMPRESTADO"