from django.shortcuts import render, get_list_or_404,redirect
from .models import Emprestimo 
from .forms import EmprestimoForm

# Create your views here.
def lista_emprestimos(request):
    emprestimos = Emprestimo.objects.all()
    return render(request, 'emprestimos/lista.html', {'emprestimos': emprestimos})

def criar_emprestimo(request):
    if request.method == 'POST':
        form = EmprestimoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_emprestimos')
    else:
        form = EmprestimoForm()
    return render(request, 'emprestimos/form.html', {'form': form})

def editar_emprestimo(request, id):
    emprestimo = get_object_or_404(Emprestimo, id=id)
    if request.method == 'POST':
        form = EmprestimoForm(request.POST, instance=emprestimo)
        if form.is_valid():
            form.save()
            return redirect('lista_emprestimos')
    else:
        form = EmprestimoForm(instance=emprestimo)
    return render(request, 'emprestimos/form.html', {'form': form})

def excluir_emprestimo(request, id):
    emprestimo = get_object_or_404(Emprestimo, id=id)
    if request.method == 'POST':
        emprestimo.delete()
        return redirect('lista_emprestimos')
    return render(request, 'emprestimos/confirm_delete.html', {'emprestimo': emprestimo})