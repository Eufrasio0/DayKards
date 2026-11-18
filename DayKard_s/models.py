
from django.db import models
from django.contrib.auth.models import User


class Baralho(models.Model):
    """Estrutura de um baralho de estudo"""

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="baralhos"
    )

    nome_baralho = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome_baralho


class Card(models.Model):
    """Estrutura de um cartão de estudo"""

    baralho = models.ForeignKey(
        Baralho,
        on_delete=models.CASCADE,
        related_name="cards"
    )

    pergunta = models.CharField(max_length=200)
    resposta = models.CharField(max_length=300)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.pergunta
