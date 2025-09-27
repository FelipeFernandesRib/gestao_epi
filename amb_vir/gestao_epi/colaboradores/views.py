from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from epis.models import Epi
from emprestimos.models import Emprestimo
from .models import Colaborador
from .forms import ColaboradorForm

def lista_colaboradores(request):
    colaboradores = Colaborador.objects.all()
    
    nome_pesquisa = request.GET.get('nome', '')
    if nome_pesquisa:
        colaboradores = colaboradores.filter(nome__icontains=nome_pesquisa)
    
    return render(request, 'colaboradores/lista.html', {
        'colaboradores': colaboradores,
        'nome_pesquisa': nome_pesquisa  # NOVO
    })

def criar_colaborador(request):
    if request.method == "POST":
        form = ColaboradorForm(request.POST)
        if form.is_valid():
            colaborador = form.save()
            messages.success(request, f"✅ Colaborador '{colaborador.nome}' cadastrado com sucesso!")
            form = ColaboradorForm()  # Limpa o formulário
        else:
            messages.error(request, "❌ Erro ao cadastrar colaborador. Verifique os dados.")
    else:
        form = ColaboradorForm()
    
    return render(request, "colaboradores/form.html", {"form": form})

def editar_colaborador(request, id):
    colaborador = get_object_or_404(Colaborador, id=id)
    
    if request.method == "POST":
        form = ColaboradorForm(request.POST, instance=colaborador)
        if form.is_valid():
            if form.has_changed():  # VERIFICA SE HOUVE ALTERAÇÕES
                form.save()
                messages.success(request, "✅ Colaborador atualizado com sucesso!")
            else:
                messages.info(request, "ℹ️ Nenhuma alteração foi realizada.")
            return redirect('lista_colaboradores')
        else:
            messages.error(request, "❌ Erro ao atualizar colaborador. Verifique os dados.")
    else:
        form = ColaboradorForm(instance=colaborador)
    
    return render(request, 'colaboradores/form.html', {
        'form': form,
        'colaborador': colaborador  # Para o template saber que é edição
    })


def excluir_colaborador(request, id):
    colaborador = get_object_or_404(Colaborador, id=id)
    
    if request.method == "POST":
        colaborador.delete()
        messages.success(request, "✅ Colaborador excluído com sucesso!")
        return redirect('lista_colaboradores')
    
    return render(request, 'colaboradores/confirm_delete.html', {'colaborador': colaborador})

def home(request):
    total_colaboradores = Colaborador.objects.count()
    total_epis = Epi.objects.count()
    
    # CORREÇÃO 1: Empréstimos Ativos - apenas os que PRECISAM ser devolvidos (status EMPRESTADO)
    emprestimos_ativos = Emprestimo.objects.filter(status='EMPRESTADO').count()
    
    # CORREÇÃO 2: EPIs com Baixo Estoque - considera quantidade DISPONÍVEL, não total
    epis_baixo_estoque = 0
    todos_epis = Epi.objects.all()
    
    for epi in todos_epis:
        disponivel = epi.quantidade_disponivel
        total = epi.quantidade_total
        
        # Considera baixo estoque se tiver menos de 20% disponível OU menos de 5 unidades
        if disponivel < max(5, total * 0.2):
            epis_baixo_estoque += 1
    
    context = {
        'total_colaboradores': total_colaboradores,
        'total_epis': total_epis,
        'emprestimos_ativos': emprestimos_ativos,
        'epis_baixo_estoque': epis_baixo_estoque,
    }
    return render(request, 'colaboradores/home.html', context)