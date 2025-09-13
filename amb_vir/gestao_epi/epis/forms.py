from django import forms
from .models import Epi

class EpiForm(forms.ModelForm):
    class Meta:
        model = Epi
        fields = ['nome', 'tipo', 'certificado_aprovacao', 'quantidade_total', 'validade', 'descricao']
        widgets = {
            'validade': forms.DateInput(attrs={'type': 'date'}),
        }