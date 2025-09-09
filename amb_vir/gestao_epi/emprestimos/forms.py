from django.forms import ModelForm
from .models import Emprestimo

class EmprestimoForm(ModelForm):
    class Meta:
        model = Emprestimo
        fields = ['colaborador', 'epi', 'data_devolucao']