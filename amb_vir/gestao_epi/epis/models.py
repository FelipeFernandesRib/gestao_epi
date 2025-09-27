from django.db import models
from django.db.models import Q, Sum

class Epi(models.Model):
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)
    certificado_aprovacao = models.CharField(max_length=20)
    quantidade_total = models.PositiveIntegerField(default=0)
    quantidade_danificada = models.PositiveIntegerField(default=0)  # NOVO CAMPO
    validade = models.DateField(null=True, blank=True)
    descricao = models.TextField(blank=True)

    @property
    def quantidade_disponivel(self):
        # CORREÇÃO CRÍTICA: Subtrai emprestados E danificados
        emprestados_count = self.emprestimo_set.filter(
            Q(status="EMPRESTADO") | Q(status="EM_USO") | Q(status="FORNECIDO")
        ).aggregate(total_emprestado=Sum('quantidade'))['total_emprestado'] or 0
        
        return self.quantidade_total - emprestados_count - self.quantidade_danificada

    @property
    def quantidade_perdida(self):
        return self.emprestimo_set.filter(status="PERDIDO").aggregate(total_perdido=Sum('quantidade'))['total_perdido'] or 0

    def __str__(self):
        return f"{self.nome} (Total: {self.quantidade_total}, Disp: {self.quantidade_disponivel}, Danif: {self.quantidade_danificada})"