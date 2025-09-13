from django.contrib import messages  # ✅ CORRETO - Adicione esta importação
from django.shortcuts import render, redirect, get_object_or_404
from .models import Epi
from .forms import EpiForm

def lista_epis(request):
    epis = Epi.objects.all()
    return render(request, 'epis/lista.html', {'epis': epis})

def criar_epi(request):
    if request.method == 'POST':
        form = EpiForm(request.POST)
        if form.is_valid():
            epi = form.save()
            messages.success(request, f'✅ EPI "{epi.nome}" cadastrado com sucesso!')
            
            # LIMPA O FORMULÁRIO para novo cadastro (em vez de redirect)
            form = EpiForm()
        else:
            messages.error(request, '❌ Erro ao cadastrar EPI. Verifique os dados.')
    else:
        form = EpiForm()
    
    return render(request, 'epis/form.html', {'form': form})

def editar_epi(request, pk):
    epi = get_object_or_404(Epi, pk=pk)
    if request.method == 'POST':
        form = EpiForm(request.POST, instance=epi)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ EPI atualizado com sucesso!')  # ✅ Adicione mensagem
            return redirect('lista_epis')
        else:
            messages.error(request, '❌ Erro ao atualizar EPI.')  # ✅ Adicione mensagem
    else:
        form = EpiForm(instance=epi)
    return render(request, 'epis/form.html', {'form': form})

def excluir_epi(request, pk):
    epi = get_object_or_404(Epi, pk=pk)
    if request.method == 'POST':
        epi.delete()
        messages.success(request, '✅ EPI excluído com sucesso!')  # ✅ Adicione mensagem
        return redirect('lista_epis')
    return render(request, 'epis/confirm_delete.html', {'epi': epi})