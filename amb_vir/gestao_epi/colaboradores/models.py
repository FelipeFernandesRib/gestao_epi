from django.db import models

# Create your models here.
from django.db import models

class Colaborador(models.Model):
    nome = models.CharField(max_length=100)
    matricula = models.CharField(max_length=20, unique=True)
    cargo = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nome} ({self.matricula})"