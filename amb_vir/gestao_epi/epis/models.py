from django.db import models

# Create your models here.
class Epi(models.Model):
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)
    certificado_aprovacao = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.nome} - CA: {self.certificado_aprovacao}"