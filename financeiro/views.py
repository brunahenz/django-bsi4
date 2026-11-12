
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Conta, Categoria, Lancamento, Orcamento
from .serializers import (
    ContaSerializer,
    CategoriaSerializer,
    LancamentoSerializer,
    OrcamentoSerializer,
)
from django.shortcuts import render
from django.db.models import Sum
from decimal import Decimal


class ContaViewSet(viewsets.ModelViewSet):
    queryset = Conta.objects.all()
    serializer_class = ContaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["nome", "banco", "ativa"]
    search_fields = ["nome", "banco"]
    ordering_fields = ["nome", "saldo_inicial", "data_criacao"]


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["nome", "tipo"]
    search_fields = ["nome", "descricao"]
    ordering_fields = ["nome", "tipo"]


class LancamentoViewSet(viewsets.ModelViewSet):
    queryset = Lancamento.objects.all()
    serializer_class = LancamentoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["tipo", "data", "conta", "categoria"]
    search_fields = ["descricao", "observacao"]
    ordering_fields = ["valor", "data", "descricao"]


class OrcamentoViewSet(viewsets.ModelViewSet):
    queryset = Orcamento.objects.all()
    serializer_class = OrcamentoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["categoria", "mes", "ano"]
    search_fields = ["categoria__nome"]
    ordering_fields = ["limite", "mes", "ano"]

def dashboard(request):
    total_receitas = Lancamento.objects.filter(
        tipo="receita"
    ).aggregate(total=Sum("valor"))["total"] or Decimal("0.00")

    total_despesas = Lancamento.objects.filter(
        tipo="despesa"
    ).aggregate(total=Sum("valor"))["total"] or Decimal("0.00")

    saldo_inicial = Conta.objects.filter(
        ativa=True
    ).aggregate(total=Sum("saldo_inicial"))["total"] or Decimal("0.00")

    saldo_total = saldo_inicial + total_receitas - total_despesas

    ultimos_lancamentos = Lancamento.objects.order_by("-data", "-id")[:5]

    contexto = {
        "saldo_total": saldo_total,
        "total_receitas": total_receitas,
        "total_despesas": total_despesas,
        "ultimos_lancamentos": ultimos_lancamentos,
    }

    return render(request, "financeiro/dashboard.html", contexto)
