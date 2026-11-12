from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Conta(models.Model):
    nome = models.CharField(max_length=100)
    banco = models.CharField(max_length=100, blank=True)
    saldo_inicial = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(Decimal("0"))]
    )
    ativa = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conta {self.banco}"


class Categoria(models.Model):
    TIPOS = [
        ("receita", "Receita"),
        ("despesa", "Despesa"),
    ]

    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=10, choices=TIPOS)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nome} - {self.tipo}"


class Lancamento(models.Model):
    TIPOS = [
        ("receita", "Receita"),
        ("despesa", "Despesa"),
    ]

    descricao = models.CharField(max_length=200)
    valor = models.DecimalField(
        max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))]
    )
    tipo = models.CharField(max_length=10, choices=TIPOS)
    data = models.DateField()
    conta = models.ForeignKey(
        Conta, on_delete=models.PROTECT, related_name="lancamentos"
    )
    categoria = models.ForeignKey(
        Categoria, on_delete=models.PROTECT, related_name="lancamentos"
    )
    observacao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.descricao} - R$ {self.valor}"


class Orcamento(models.Model):
    categoria = models.ForeignKey(
        Categoria, on_delete=models.PROTECT, related_name="orcamentos"
    )
    limite = models.DecimalField(
        max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))]
    )
    mes = models.PositiveSmallIntegerField()
    ano = models.PositiveSmallIntegerField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.categoria.nome} - {self.mes}/{self.ano}"
