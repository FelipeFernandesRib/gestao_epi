from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Emprestimo
from .forms import EmprestimoForm
from colaboradores.models import Colaborador
from epis.models import Epi

def lista_emprestimos(request):
    emprestimos = Emprestimo.objects.all().order_by('-data_emprestimo')
    return render(request, 'emprestimos/lista.html', {'emprestimos': emprestimos})

def criar_emprestimo(request):
    colaboradores = Colaborador.objects.all()
    epis = Epi.objects.all()
    
    if request.method == "POST":
        form = EmprestimoForm(request.POST)
        if form.is_valid():
            try:
                emprestimo = form.save()
                messages.success(request, "✅ Empréstimo registrado com sucesso!")
                return redirect("lista_emprestimos")
            except Exception as e:
                messages.error(request, f"❌ Erro: {str(e)}")
        else:
            # Debug: mostrar erros do formulário
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Erro no campo {field}: {error}")
    else:
        form = EmprestimoForm()

    return render(request, "emprestimos/form.html", {
        "form": form,
        "colaboradores": colaboradores,
        "epis": epis,
        "emprestimo": None  # Para diferenciar criação vs edição
    })

def editar_emprestimo(request, id):
    emprestimo = get_object_or_404(Emprestimo, id=id)
    colaboradores = Colaborador.objects.all()
    epis = Epi.objects.all()

    if request.method == 'POST':
        form = EmprestimoForm(request.POST, instance=emprestimo)
        if form.is_valid():
            if form.has_changed():
                try:
                    form.save()
                    messages.success(request, "✅ Empréstimo atualizado com sucesso!")
                except Exception as e:
                    messages.error(request, f"❌ Erro ao atualizar empréstimo: {str(e)}")
            else:
                messages.info(request, "ℹ️ Nenhuma alteração foi realizada.")
            return redirect('lista_emprestimos')
        else:
            # Debug: mostrar erros do formulário
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Erro no campo {field}: {error}")
    else:
        form = EmprestimoForm(instance=emprestimo)

    return render(request, 'emprestimos/form.html', {
        'form': form, 
        'emprestimo': emprestimo,  # Passa o objeto emprestimo para o template
        "colaboradores": colaboradores,
        "epis": epis
    })

def devolver_emprestimo(request, pk):
    emprestimo = get_object_or_404(Emprestimo, pk=pk)
    
    if request.method == 'POST':
        status = request.POST.get('status', 'DEVOLVIDO')
        observacao = request.POST.get('observacao', '')
        
        if status in ['DANIFICADO', 'PERDIDO'] and not observacao:
            messages.error(request, "❌ Observação é obrigatória para status Danificado ou Perdido.")
            return redirect('lista_emprestimos')
        
        try:
            # CORREÇÃO CRÍTICA: Atualizar estoque de danificados
            if status == 'DANIFICADO':
                emprestimo.epi.quantidade_danificada += emprestimo.quantidade
                emprestimo.epi.save()
                messages.success(request, f"✅ EPI devolvido como DANIFICADO. {emprestimo.quantidade} unidade(s) removida(s) do estoque útil.")
            elif status == 'PERDIDO':
                messages.success(request, f"✅ EPI marcado como PERDIDO. {emprestimo.quantidade} unidade(s) considerada(s) como perda.")
            else:
                messages.success(request, f"✅ EPI devolvido com sucesso! Status: {emprestimo.get_status_display()}")
            
            emprestimo.devolver(status=status, observacao=observacao)
            
        except Exception as e:
            messages.error(request, f"❌ Erro ao devolver EPI: {str(e)}")
    else:
        return render(request, 'emprestimos/devolver.html', {'emprestimo': emprestimo})
    
    return redirect('lista_emprestimos')

def marcar_perdido(request, pk):
    emprestimo = get_object_or_404(Emprestimo, pk=pk)
    
    if emprestimo.status in ['EMPRESTADO', 'EM_USO']:
        try:
            emprestimo.status = 'PERDIDO'
            emprestimo.data_devolucao = timezone.now()
            emprestimo.observacao_devolucao = 'EPI marcado como perdido'
            emprestimo.save()
            
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