from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from epis.models import Epi
from emprestimos.models import Emprestimo
from .models import Colaborador
from .forms import ColaboradorForm



def lista_colaboradores(request):
    colaboradores = Colaborador.objects.all()
    return render(request, 'colaboradores/lista.html', {'colaboradores': colaboradores})

def criar_colaborador(request):
    if request.method == "POST":
        form = ColaboradorForm(request.POST)
        if form.is_valid():
            colaborador = form.save()
            messages.success(request, f"✅ Colaborador '{colaborador.nome}' cadastrado com sucesso!")
            
            # ⚠️ REMOVA O REDIRECT e limpe o formulário para novo cadastro
            form = ColaboradorForm()  # Limpa o formulário em vez de redirecionar
            
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
            form.save()
            messages.success(request, "✅ Colaborador atualizado com sucesso!")
            return redirect('lista_colaboradores')
        else:
            messages.error(request, "❌ Erro ao atualizar colaborador.")
    else:
        form = ColaboradorForm(instance=colaborador)
    
    return render(request, 'colaboradores/form.html', {'form': form})

def excluir_colaborador(request, id):
    colaborador = get_object_or_404(Colaborador, id=id)
    
    if request.method == "POST":
        colaborador.delete()
        messages.success(request, "✅ Colaborador excluído com sucesso!")
        return redirect('lista_colaboradores')
    
    return render(request, 'colaboradores/confirm_delete.html', {'colaborador': colaborador})

def home(request):
    return render(request, 'colaboradores/home.html')

def home(request):
    total_colaboradores = Colaborador.objects.count()
    total_epis = Epi.objects.count()
    # Linha corrigida para 'quantidade_total__lte'
    epis_baixo_estoque = Epi.objects.filter(quantidade_total__lte=10).count()
    emprestimos_ativos = Emprestimo.objects.filter(data_devolucao__isnull=True).count()
    
    context = {
        'total_colaboradores': total_colaboradores,
        'total_epis': total_epis,
        'emprestimos_ativos': emprestimos_ativos,
        'epis_baixo_estoque': epis_baixo_estoque, # Adicionado ao contexto
    }
    return render(request, 'colaboradores/home.html', context)