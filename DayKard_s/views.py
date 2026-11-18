from django.shortcuts import render
from DayKard_s.models import Baralho
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Baralho, Card
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.http import require_POST
from django.contrib import messages

# Create your views here.

def home(request):
    """Página inicial do site"""
    return render(request, 'DayKard_s/home.html')

def login_user(request):

    if request.method == "POST":

        # Captura os dados enviados pelo formulário
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Verifica as credenciais
        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("dashboard")

        else:
            messages.error(
                request,
                "Nome de usuário ou senha incorretos."
            )

    # Se for GET, apenas apresenta a página
    return render(request, "DayKard_s/login.html")

def view_list_baralho(request):
    """Exibe a lista de baralhos do usuário"""
    baralhos = Baralho.objects.order_by('date_added')
    context = {'baralhos': baralhos}
    return render(request, 'DayKard_s/view_list_baralho.html', context)


def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('home')

        return render(request, 'login.html', {
            'erro': 'Usuário ou senha incorretos.'
        })

    return render(request, 'login.html')

def cadastro_user(request):
    return render(request, 'DayKard_s/cadastro.html')


def cadastro_user(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Verifica se as senhas são iguais
        if password != confirm_password:
            messages.error(request, "As senhas não coincidem.")
            return redirect("cadastro")

        # Verifica se o usuário já existe
        if User.objects.filter(username=username).exists():
            messages.error(request, "Nome de usuário já cadastrado.")
            return redirect("cadastro")

        # Verifica se o email já existe
        if User.objects.filter(email=email).exists():
            messages.error(request, "E-mail já cadastrado.")
            return redirect("cadastro")

        # Cria o usuário
        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(request, "Conta criada com sucesso!")

        return redirect("login_user")

    return render(request, "DayKard_s/cadastro.html")


@login_required
def dashboard(request):
    # Busca somente os baralhos do usuário conectado
    baralhos = Baralho.objects.filter(
        usuario=request.user
    ).order_by("-date_added")

    # Conta todos os cards dos baralhos desse usuário
    total_cards = Card.objects.filter(
        baralho__usuario=request.user
    ).count()

    context = {
        "baralhos": baralhos,
        "total_cards": total_cards,
    }

    return render(
        request,
        "DayKard_s/dashboard.html",
        context
    )


@login_required
@require_POST
def criar_baralho(request):
    nome = request.POST.get("nome_baralho", "").strip()

    if not nome:
        messages.error(request, "Informe um nome para o baralho.")
        return redirect("dashboard")

    Baralho.objects.create(
        usuario=request.user,
        nome_baralho=nome
    )

    messages.success(request, "Baralho criado com sucesso!")

    return redirect("dashboard")


@login_required
@require_POST
def criar_card(request, baralho_id):
    # Garante que o baralho pertence ao usuário conectado
    baralho = get_object_or_404(
        Baralho,
        id=baralho_id,
        usuario=request.user
    )

    pergunta = request.POST.get("pergunta", "").strip()
    resposta = request.POST.get("resposta", "").strip()

    if not pergunta or not resposta:
        messages.error(request, "Preencha a pergunta e a resposta.")
        return redirect("dashboard")

    Card.objects.create(
        baralho=baralho,
        pergunta=pergunta,
        resposta=resposta
    )

    messages.success(request, "Card adicionado com sucesso!")

    return redirect("dashboard")


@login_required
@require_POST
def deletar_baralho(request, baralho_id):
    baralho = get_object_or_404(
        Baralho,
        id=baralho_id,
        usuario=request.user
    )

    baralho.delete()

    messages.success(request, "Baralho excluído com sucesso!")

    return redirect("dashboard")


@login_required
@require_POST
def deletar_card(request, card_id):
    # Busca o card somente se pertencer a um baralho do usuário
    card = get_object_or_404(
        Card,
        id=card_id,
        baralho__usuario=request.user
    )

    card.delete()

    messages.success(request, "Card excluído com sucesso!")

    return redirect("dashboard")


@login_required
@require_POST
def logout_user(request):
    logout(request)
    return redirect("login_user")


@login_required
def revisar_baralho(request, baralho_id, card_id=None):

    baralho = get_object_or_404(
        Baralho,
        id=baralho_id,
        usuario=request.user
    )

    cards = Card.objects.filter(
        baralho=baralho
    ).order_by("id")

    # Verifica se existem cartões
    if not cards.exists():
        return render(
            request,
            "DayKard_s/revisar.html",
            {
                "baralho": baralho,
                "card": None,
            }
        )

    # Se nenhum cartão foi informado, começa pelo primeiro
    if card_id is None:
        card = cards.first()

    else:
        card = get_object_or_404(
            Card,
            id=card_id,
            baralho=baralho
        )

    # Procura o próximo cartão
    proximo_card = cards.filter(
        id__gt=card.id
    ).first()

    # Se chegou ao último, volta para o primeiro
    if proximo_card is None:
        proximo_card = cards.first()

    context = {
        "baralho": baralho,
        "card": card,
        "proximo_card": proximo_card,
        "total_cards": cards.count(),
    }

    return render(
        request,
        "DayKard_s/revisar.html",
        context
    )