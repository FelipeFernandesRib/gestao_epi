from django import forms
from django.utils import timezone
from .models import Emprestimo
from epis.models import Epi

class EmprestimoForm(forms.ModelForm):
    class Meta:
        model = Emprestimo
        fields = ['colaborador', 'epi', 'quantidade', 'data_prevista_devolucao', 'status', 'data_devolucao', 'observacao_devolucao']
        widgets = {
            'data_prevista_devolucao': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'data_devolucao': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'observacao_devolucao': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Descreva o estado do EPI devolvido...'}),
            'status': forms.Select(attrs={'class': 'form-select', 'onchange': 'toggleCamposDevolucao()'}),
            'colaborador': forms.Select(attrs={'class': 'form-select'}),
            'epi': forms.Select(attrs={'class': 'form-select', 'onchange': 'atualizarInfoEstoque()'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        
        if not instance:
            self.fields['status'].choices = [
                ('EMPRESTADO', 'Emprestado'),
                ('FORNECIDO', 'Fornecido'),
            ]
            self.fields['data_devolucao'].widget = forms.HiddenInput()
            self.fields['observacao_devolucao'].widget = forms.HiddenInput()
        else:
            self.fields['data_devolucao'].required = False
            self.fields['observacao_devolucao'].required = False

    def clean(self):
        cleaned_data = super().clean()
        epi_id = cleaned_data.get("epi").id  # Pega o ID do EPI para garantir que estamos acessando a instância correta
        quantidade = cleaned_data.get("quantidade")
        status = cleaned_data.get("status")
        data_prevista_devolucao = cleaned_data.get("data_prevista_devolucao")
        data_devolucao = cleaned_data.get('data_devolucao')
        observacao = cleaned_data.get('observacao_devolucao')

        try:
            # Pega a instância do EPI novamente para garantir que a propriedade existe
            epi_instance = Epi.objects.get(id=epi_id)
            if quantidade > epi_instance.quantidade_disponivel:
                raise forms.ValidationError(
                    f"Quantidade solicitada ({quantidade}) maior que a disponível ({epi_instance.quantidade_disponivel})"
                )
        except Epi.DoesNotExist:
            raise forms.ValidationError("EPI selecionado não existe.")
        
        if quantidade <= 0:
            raise forms.ValidationError("A quantidade deve ser maior que zero.")

        if data_prevista_devolucao and data_prevista_devolucao <= timezone.now():
            raise forms.ValidationError({
                'data_prevista_devolucao': 'A data prevista para devolução deve ser posterior à data e hora atuais.'
            })

        if status in ['DEVOLVIDO', 'DANIFICADO', 'PERDIDO']:
            if not data_devolucao:
                raise forms.ValidationError({
                    'data_devolucao': 'Data de devolução é obrigatória para este status.'
                })
            
            if status in ['DANIFICADO', 'PERDIDO'] and not observacao:
                raise forms.ValidationError({
                    'observacao_devolucao': 'Observação é obrigatória para status Danificado ou Perdido.'
                })

        return cleaned_data