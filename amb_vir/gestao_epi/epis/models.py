from django.db import models
from django.db.models import Q, Sum

class Epi(models.Model):
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)
    certificado_aprovacao = models.CharField(max_length=20)
    quantidade_total = models.PositiveIntegerField(default=0)
    validade = models.DateField(null=True, blank=True)
    descricao = models.TextField(blank=True)

    @property
    def quantidade_disponivel(self):
        # Calcula o total emprestado que ainda não foi devolvido
        emprestados_count = self.emprestimo_set.filter(
            Q(status="EMPRESTADO") | Q(status="EM_USO") | Q(status="FORNECIDO")
        ).aggregate(total_emprestado=Sum('quantidade'))['total_emprestado'] or 0
        return self.quantidade_total - emprestados_count

    @property
    def quantidade_perdida(self):
        # Para acompanhamento: quantos EPIs foram perdidos
        return self.emprestimo_set.filter(status="PERDIDO").aggregate(total_perdido=Sum('quantidade'))['total_perdido'] or 0

    def __str__(self):
        return f"{self.nome}"