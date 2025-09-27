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
            # Novo empréstimo: só mostra EMPRESTADO e FORNECIDO
            self.fields['status'].choices = [
                ('EMPRESTADO', 'Emprestado'),
                ('FORNECIDO', 'Fornecido'),
            ]
            self.fields['data_devolucao'].widget = forms.HiddenInput()
            self.fields['observacao_devolucao'].widget = forms.HiddenInput()
        else:
            # Edição: mostra todos os status
            self.fields['data_devolucao'].required = False
            self.fields['observacao_devolucao'].required = False

    def clean(self):
        cleaned_data = super().clean()
        epi = cleaned_data.get("epi")
        quantidade = cleaned_data.get("quantidade")
        status = cleaned_data.get("status")
        data_prevista_devolucao = cleaned_data.get("data_prevista_devolucao")
        observacao = cleaned_data.get('observacao_devolucao')

        # Validação de quantidade vs estoque (CORRIGIDA para edição)
        if epi and quantidade is not None:
            # Se for edição, adiciona a quantidade atual ao estoque disponível
            if self.instance and self.instance.pk:
                quantidade_disponivel = epi.quantidade_disponivel + self.instance.quantidade
            else:
                quantidade_disponivel = epi.quantidade_disponivel

            if quantidade > quantidade_disponivel:
                raise forms.ValidationError({
                    'quantidade': f"Quantidade solicitada ({quantidade}) maior que a disponível ({quantidade_disponivel})"
                })
        
        if quantidade and quantidade <= 0:
            raise forms.ValidationError({
                'quantidade': 'A quantidade deve ser maior que zero.'
            })

        # Validação de data prevista
        if data_prevista_devolucao and data_prevista_devolucao <= timezone.now():
            raise forms.ValidationError({
                'data_prevista_devolucao': 'A data prevista para devolução deve ser posterior à data e hora atuais.'
            })

        # Validações condicionais para status de devolução (CORREÇÃO CRÍTICA)
        if status in ['DANIFICADO', 'PERDIDO'] and not observacao:
            raise forms.ValidationError({
                'observacao_devolucao': 'Observação é obrigatória para status Danificado ou Perdido.'
            })

        # REMOVIDO: Validação de data_devolucao - é automática via método devolver()

        return cleaned_data