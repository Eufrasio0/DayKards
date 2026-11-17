from django.shortcuts import render
from DayKard_s.models import Baralho

# Create your views here.

def home(request):
    """Página inicial do site"""
    return render(request, 'DayKard_s/home.html')

def login_user(request):
    """Página de login do site"""
    return render(request, 'DayKard_s/login.html')

def view_list_baralho(request):
    """Exibe a lista de baralhos do usuário"""
    baralhos = Baralho.objects.order_by('date_added')
    context = {'baralhos': baralhos}
    return render(request, 'DayKard_s/view_list_baralho.html', context)