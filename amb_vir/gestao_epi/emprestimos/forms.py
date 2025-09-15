from django import forms
from django.utils import timezone
from .models import Emprestimo

class EmprestimoForm(forms.ModelForm):
    class Meta:
        model = Emprestimo
        fields = ['colaborador', 'epi', 'quantidade', 'data_prevista_devolucao', 'status', 'data_devolucao', 'observacao_devolucao']
        widgets = {
            'data_prevista_devolucao': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'data_devolucao': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'observacao_devolucao': forms.Textarea(attrs={'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        
        # Para novo empréstimo, ocultar alguns campos
        if not instance:
            self.fields['status'].choices = [
                ('EMPRESTADO', 'Emprestado'),
                ('EM USO', 'Em Uso'),
                ('FORNECIDO', 'Fornecido'),
            ]
            self.fields['data_devolucao'].widget = forms.HiddenInput()
            self.fields['observacao_devolucao'].widget = forms.HiddenInput()
        else:
            # Para edição, mostrar todos os campos
            self.fields['data_devolucao'].required = False
            self.fields['observacao_devolucao'].required = False

    def clean(self):
        cleaned_data = super().clean()
        epi = cleaned_data.get("epi")
        quantidade = cleaned_data.get("quantidade")
        status = cleaned_data.get("status")
        data_prevista_devolucao = cleaned_data.get("data_prevista_devolucao")

        # Validação de quantidade
        if epi and quantidade:
            if quantidade > epi.quantidade_disponivel:
                raise forms.ValidationError(
                    f"Quantidade solicitada ({quantidade}) maior que a disponível ({epi.quantidade_disponivel})"
                )

        # Validação de data prevista
        if data_prevista_devolucao and data_prevista_devolucao <= timezone.now():
            raise forms.ValidationError({
                'data_prevista_devolucao': 'A data prevista para devolução deve ser posterior à data e hora atuais.'
            })

        # Validação de campos condicionais
        if status in ['DEVOLVIDO', 'DANIFICADO', 'PERDIDO']:
            data_devolucao = cleaned_data.get('data_devolucao')
            if not data_devolucao:
                raise forms.ValidationError({
                    'data_devolucao': 'Data de devolução é obrigatória para este status.'
                })

        return cleaned_data