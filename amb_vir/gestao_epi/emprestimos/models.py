from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from colaboradores.models import Colaborador
from epis.models import Epi

class Emprestimo(models.Model):
    STATUS_CHOICES = [
        ('EMPRESTADO', 'Emprestado'),
        ('EM_USO', 'Em Uso'),
        ('FORNECIDO', 'Fornecido'),
        ('DEVOLVIDO', 'Devolvido'),
        ('DANIFICADO', 'Danificado'),
        ('PERDIDO', 'Perdido'),
    ]

    colaborador = models.ForeignKey('colaboradores.Colaborador', on_delete=models.CASCADE)
    epi = models.ForeignKey('epis.Epi', on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)
    data_emprestimo = models.DateTimeField(auto_now_add=True)
    data_prevista_devolucao = models.DateTimeField(null=True, blank=True)
    data_devolucao = models.DateTimeField(null=True, blank=True)
    observacao_devolucao = models.TextField(blank=True, verbose_name="Observação na Devolução")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='EMPRESTADO')

    def clean(self):
        """Validação personalizada para datas"""
        if self.data_prevista_devolucao and self.data_prevista_devolucao <= timezone.now():
            raise ValidationError({
                'data_prevista_devolucao': 'A data prevista para devolução deve ser posterior à data e hora atuais.'
            })

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def devolver(self, status='DEVOLVIDO', observacao=''):
        """Método para devolução do EPI"""
        if self.status in ['EMPRESTADO', 'EM_USO']:
            self.status = status
            self.data_devolucao = timezone.now()
            self.observacao_devolucao = observacao
            self.save()
    def is_em_andamento(self):
        return self.status in ['EMPRESTADO', 'EM_USO']

    def __str__(self):
        return f"{self.colaborador.nome} - {self.epi.nome} ({self.quantidade}x - {self.get_status_display()})"