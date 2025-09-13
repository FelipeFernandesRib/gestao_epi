from django import forms
from .models import Emprestimo

class EmprestimoForm(forms.ModelForm):
    class Meta:
        model = Emprestimo
        fields = ['colaborador', 'epi', 'quantidade']

    def clean(self):
        cleaned_data = super().clean()
        epi = cleaned_data.get("epi")
        quantidade = cleaned_data.get("quantidade")

        if epi and quantidade:
            if quantidade > epi.quantidade_disponivel:
                raise forms.ValidationError(
                    f"Quantidade solicitada ({quantidade}) maior que a disponível ({epi.quantidade_disponivel})"
                )

        return cleaned_data