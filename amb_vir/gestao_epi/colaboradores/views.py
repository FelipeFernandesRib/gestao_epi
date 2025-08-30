from django.shortcuts import render, get_object_or_404, redirect
from .models import Colaborador
from .forms import ColaboradorForm

def lista_colaboradores(request):
    colaboradores = Colaborador.objects.all()
    return render(request, 'colaboradores/lista.html', {'colaboradores': colaboradores})

def criar_colaborador(request):
    if request.method == 'POST':
        form = ColaboradorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_colaboradores')
    else:
        form = ColaboradorForm()
    return render(request, 'colaboradores/form.html', {'form': form})

def editar_colaborador(request, id):
    colaborador = get_object_or_404(Colaborador, id=id)
    if request.method == 'POST':
        form = ColaboradorForm(request.POST, instance=colaborador)
        if form.is_valid():
            form.save()
            return redirect('lista_colaboradores')
    else:
        form = ColaboradorForm(instance=colaborador)
    return render(request, 'colaboradores/form.html', {'form': form})

def excluir_colaborador(request, id):
    colaborador = get_object_or_404(Colaborador, id=id)
    if request.method == 'POST':
        colaborador.delete()
        return redirect('lista_colaboradores')
    return render(request, 'colaboradores/confirm_delete.html', {'colaborador': colaborador})

