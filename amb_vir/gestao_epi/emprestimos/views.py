from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Emprestimo
from .forms import EmprestimoForm

def lista_emprestimos(request):
    emprestimos = Emprestimo.objects.all().order_by('-data_emprestimo')
    return render(request, 'emprestimos/lista.html', {'emprestimos': emprestimos})

def criar_emprestimo(request):
    if request.method == "POST":
        form = EmprestimoForm(request.POST)
        if form.is_valid():
            try:
                emprestimo = form.save()
                messages.success(request, f"✅ Empréstimo registrado com sucesso! Status: {emprestimo.get_status_display()}")
                return redirect("lista_emprestimos")
            except Exception as e:
                messages.error(request, f"❌ Erro ao registrar empréstimo: {str(e)}")
        else:
            messages.error(request, "❌ Erro no formulário. Verifique os dados.")
    else:
        form = EmprestimoForm()
    
    return render(request, "emprestimos/form.html", {"form": form})

def editar_emprestimo(request, id):
    emprestimo = get_object_or_404(Emprestimo, id=id)

    if request.method == 'POST':
        form = EmprestimoForm(request.POST, instance=emprestimo)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "✅ Empréstimo atualizado com sucesso!")
                return redirect('lista_emprestimos')
            except Exception as e:
                messages.error(request, f"❌ Erro ao atualizar empréstimo: {str(e)}")
        else:
            messages.error(request, "❌ Erro no formulário. Verifique os dados.")
    else:
        form = EmprestimoForm(instance=emprestimo)
    
    return render(request, 'emprestimos/form.html', {'form': form, 'emprestimo': emprestimo})

def devolver_emprestimo(request, pk):
    emprestimo = get_object_or_404(Emprestimo, pk=pk)
    
    if request.method == 'POST':
        status = request.POST.get('status', 'DEVOLVIDO')
        observacao = request.POST.get('observacao', '')
        
        try:
            emprestimo.devolver(status=status, observacao=observacao)
            messages.success(request, f"✅ EPI devolvido com sucesso! Status: {emprestimo.get_status_display()}")
        except Exception as e:
            messages.error(request, f"❌ Erro ao devolver EPI: {str(e)}")
    
    return redirect('lista_emprestimos')

def marcar_perdido(request, pk):
    emprestimo = get_object_or_404(Emprestimo, pk=pk)
    
    if emprestimo.status in ['EMPRESTADO', 'EM_USO']:
        try:
            emprestimo.status = 'PERDIDO'
            emprestimo.data_devolucao = timezone.now()
            emprestimo.save()
            
            # Atualiza estoque para EPI perdido
            emprestimo.epi.quantidade_total -= emprestimo.quantidade
            emprestimo.epi.save()
            
            messages.success(request, "✅ EPI marcado como perdido e removido do estoque.")
        except Exception as e:
            messages.error(request, f"❌ Erro ao marcar como perdido: {str(e)}")
    else:
        messages.warning(request, "⚠️ Este empréstimo não pode ser marcado como perdido.")
    
    return redirect('lista_emprestimos')

def relatorios_emprestimos(request):
    colaborador_nome = request.GET.get('colaborador', '')
    status_filter = request.GET.get('status', '')
    emprestimos = Emprestimo.objects.all().order_by('-data_emprestimo')
    
    if colaborador_nome:
        emprestimos = emprestimos.filter(colaborador__nome__icontains=colaborador_nome)
    
    if status_filter:
        emprestimos = emprestimos.filter(status=status_filter)
    
    context = {
        'emprestimos': emprestimos,
        'colaborador_pesquisa': colaborador_nome,
        'status_pesquisa': status_filter,
        'total_emprestimos': emprestimos.count(),
        'status_choices': Emprestimo.STATUS_CHOICES,
    }
    
    return render(request, 'emprestimos/relatorios.html', context)