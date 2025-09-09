from django.shortcuts import render
from .models import Epi

# Create your views here.
def lista_epis(request):
    epis = Epi.objects.all()
    return render(request, 'epis/lista.html', {'epis': epis})