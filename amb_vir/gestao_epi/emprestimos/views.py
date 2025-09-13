from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .models import Emprestimo
from .forms import EmprestimoForm

def lista_emprestimos(request):
    emprestimos = Emprestimo.objects.all()
    return render(request, 'emprestimos/lista.html', {'emprestimos': emprestimos})

def criar_emprestimo(request):
    if request.method == "POST":
        form = EmprestimoForm(request.POST)
        if form.is_valid():
            emprestimo = form.save(commit=False)

            # garante que não empresta mais do que disponível
            if emprestimo.quantidade > emprestimo.epi.quantidade_disponivel:
                form.add_error('quantidade', "Quantidade solicitada maior do que a disponível.")
                return render(request, "emprestimos/form.html", {"form": form})

            emprestimo.save()
            return redirect("lista_emprestimos")
    else:
        form = EmprestimoForm()
    return render(request, "emprestimos/form.html", {"form": form})

def editar_emprestimo(request, id):
    emprestimo = get_object_or_404(Emprestimo, id=id)

    # Bloqueia edição se já devolvido ou perdido
    if emprestimo.status != "EMPRESTADO":
        messages.error(request, "Não é permitido editar um empréstimo já finalizado.")
        return redirect('lista_emprestimos')

    if request.method == 'POST':
        form = EmprestimoForm(request.POST, instance=emprestimo)
        if form.is_valid():
            form.save()
            messages.success(request, "Empréstimo atualizado com sucesso.")
            return redirect('lista_emprestimos')
    else:
        form = EmprestimoForm(instance=emprestimo)
    return render(request, 'emprestimos/form.html', {'form': form})

def devolver_emprestimo(request, pk):
    emprestimo = get_object_or_404(Emprestimo, pk=pk)
    if emprestimo.status == "EMPRESTADO":
        emprestimo.devolver()
        messages.success(request, "EPI devolvido com sucesso.")
    else:
        messages.warning(request, "Este empréstimo já foi devolvido ou está marcado como perdido.")
    return redirect('lista_emprestimos')


def marcar_perdido(request, pk):
    emprestimo = get_object_or_404(Emprestimo, pk=pk)
    if emprestimo.status == "EMPRESTADO":
        emprestimo.status = "PERDIDO"
        emprestimo.data_devolucao = timezone.now()
        emprestimo.save()
        
        # ATUALIZA A QUANTIDADE TOTAL - EPI PERDIDO DEVE SER SUBTRAÍDO DO TOTAL
        emprestimo.epi.quantidade_total -= emprestimo.quantidade
        emprestimo.epi.save()
        
        messages.success(request, "EPI marcado como perdido e removido do estoque.")
    else:
        messages.warning(request, "Este empréstimo não pode ser marcado como perdido.")
    
    return redirect('lista_emprestimos')