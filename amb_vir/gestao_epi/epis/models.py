from django.db import models

class Epi(models.Model):
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)
    certificado_aprovacao = models.CharField(max_length=20)
    quantidade_total = models.PositiveIntegerField(default=0)
    validade = models.DateField(null=True, blank=True)
    descricao = models.TextField(blank=True)

    @property
    def quantidade_disponivel(self):
        emprestados = sum(
            e.quantidade for e in self.emprestimo_set.filter(status="EMPRESTADO")
        )
        return self.quantidade_total - emprestados

    def __str__(self):
        return f"{self.nome}"
    @property
    def quantidade_disponivel(self):
        # Calcula o total emprestado que ainda não foi devolvido
        emprestados = sum(
            e.quantidade for e in self.emprestimo_set.filter(status="EMPRESTADO")
        )
        # EPIs perdidos já foram subtraídos da quantidade_total na view marcar_perdido
        return self.quantidade_total - emprestados
    
    @property
    def quantidade_perdida(self):
        # Para acompanhamento: quantos EPIs foram perdidos
        return sum(
            e.quantidade for e in self.emprestimo_set.filter(status="PERDIDO")
        )