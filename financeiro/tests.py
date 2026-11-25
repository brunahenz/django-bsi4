from decimal import Decimal

from django.test import TestCase

from .models import Conta, Categoria
from .serializers import (
    ContaSerializer,
    CategoriaSerializer,
    LancamentoSerializer,
    OrcamentoSerializer,
)
from rest_framework.test import APITestCase
from django.urls import reverse

class ContaSerializerTest(TestCase):

    def test_criar_conta_valida(self):
        serializer = ContaSerializer(data={
            "nome": "Conta principal",
            "banco": "Nubank",
            "saldo_inicial": "1000.00",
            "ativa": True,
        })

        self.assertTrue(serializer.is_valid())

    def test_impedir_saldo_inicial_negativo(self):
        serializer = ContaSerializer(data={
            "nome": "Conta principal",
            "banco": "Nubank",
            "saldo_inicial": "-100.00",
            "ativa": True,
        })

        self.assertFalse(serializer.is_valid())


class CategoriaSerializerTest(TestCase):

    def test_criar_categoria_valida(self):
        serializer = CategoriaSerializer(data={
            "nome": "Alimentação",
            "tipo": "despesa",
            "descricao": "Gastos com alimentação",
        })

        self.assertTrue(serializer.is_valid())


class LancamentoSerializerTest(TestCase):

    def setUp(self):
        self.conta = Conta.objects.create(
            nome="Conta principal",
            banco="Nubank",
            saldo_inicial=Decimal("1000.00"),
        )

        self.categoria_despesa = Categoria.objects.create(
            nome="Alimentação",
            tipo="despesa",
        )

        self.categoria_receita = Categoria.objects.create(
            nome="Salário",
            tipo="receita",
        )

    def test_criar_lancamento_valido(self):
        serializer = LancamentoSerializer(data={
            "descricao": "Compra no mercado",
            "valor": "150.00",
            "tipo": "despesa",
            "data": "2026-11-16",
            "conta": self.conta.id,
            "categoria": self.categoria_despesa.id,
        })

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_impedir_categoria_com_tipo_diferente(self):
        serializer = LancamentoSerializer(data={
            "descricao": "Compra no mercado",
            "valor": "150.00",
            "tipo": "despesa",
            "data": "2026-11-16",
            "conta": self.conta.id,
            "categoria": self.categoria_receita.id,
        })

        self.assertFalse(serializer.is_valid())
        self.assertIn("categoria", serializer.errors)

    def test_impedir_lancamento_com_valor_zero(self):
        serializer = LancamentoSerializer(data={
            "descricao": "Compra no mercado",
            "valor": "0.00",
            "tipo": "despesa",
            "data": "2026-11-16",
            "conta": self.conta.id,
            "categoria": self.categoria_despesa.id,
        })

        self.assertFalse(serializer.is_valid())
        self.assertIn("valor", serializer.errors)

    def test_impedir_lancamento_com_valor_negativo(self):
        serializer = LancamentoSerializer(data={
            "descricao": "Compra no mercado",
            "valor": "-50.00",
            "tipo": "despesa",
            "data": "2026-11-16",
            "conta": self.conta.id,
            "categoria": self.categoria_despesa.id,
        })

        self.assertFalse(serializer.is_valid())
        self.assertIn("valor", serializer.errors)


class OrcamentoSerializerTest(TestCase):

    def setUp(self):
        self.categoria_despesa = Categoria.objects.create(
            nome="Alimentação",
            tipo="despesa",
        )

        self.categoria_receita = Categoria.objects.create(
            nome="Salário",
            tipo="receita",
        )

    def test_criar_orcamento_valido(self):
        serializer = OrcamentoSerializer(data={
            "categoria": self.categoria_despesa.id,
            "limite": "800.00",
            "mes": 11,
            "ano": 2026,
        })

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_impedir_orcamento_para_categoria_de_receita(self):
        serializer = OrcamentoSerializer(data={
            "categoria": self.categoria_receita.id,
            "limite": "800.00",
            "mes": 11,
            "ano": 2026,
        })

        self.assertFalse(serializer.is_valid())
        self.assertIn("categoria", serializer.errors)

    def test_impedir_mes_invalido(self):
        serializer = OrcamentoSerializer(data={
            "categoria": self.categoria_despesa.id,
            "limite": "800.00",
            "mes": 13,
            "ano": 2026,
        })

        self.assertFalse(serializer.is_valid())
        self.assertIn("mes", serializer.errors)

    def test_impedir_ano_invalido(self):
        serializer = OrcamentoSerializer(data={
            "categoria": self.categoria_despesa.id,
            "limite": "800.00",
            "mes": 11,
            "ano": 1999,
        })

        self.assertFalse(serializer.is_valid())
        self.assertIn("ano", serializer.errors)

    def test_impedir_orcamento_com_limite_zero(self):
        serializer = OrcamentoSerializer(data={
            "categoria": self.categoria_despesa.id,
            "limite": "0.00",
            "mes": 11,
            "ano": 2026,
        })

        self.assertFalse(serializer.is_valid())
        self.assertIn("limite", serializer.errors)


class FinanceiroAPITest(APITestCase):

    def setUp(self):
        self.conta = Conta.objects.create(
            nome="Conta principal",
            banco="Nubank",
            saldo_inicial=Decimal("1000.00"),
        )

        self.categoria_despesa = Categoria.objects.create(
            nome="Alimentação",
            tipo="despesa",
        )

        self.categoria_receita = Categoria.objects.create(
            nome="Salário",
            tipo="receita",
        )

        from .models import Lancamento

        Lancamento.objects.create(
            descricao="Compra no mercado",
            valor=Decimal("150.00"),
            tipo="despesa",
            data="2026-11-16",
            conta=self.conta,
            categoria=self.categoria_despesa,
        )

        Lancamento.objects.create(
            descricao="Conta de luz",
            valor=Decimal("200.00"),
            tipo="despesa",
            data="2026-11-15",
            conta=self.conta,
            categoria=self.categoria_despesa,
        )

    def test_crud_conta_pela_api(self):
        url = reverse("conta-list")

        resposta = self.client.post(url, {
            "nome": "Conta de teste",
            "banco": "Inter",
            "saldo_inicial": "500.00",
            "ativa": True,
        })

        self.assertEqual(resposta.status_code, 201)

        conta_id = resposta.data["id"]
        detalhe = reverse("conta-detail", args=[conta_id])

        resposta = self.client.get(detalhe)
        self.assertEqual(resposta.status_code, 200)

        resposta = self.client.patch(detalhe, {
            "nome": "Conta atualizada",
        })
        self.assertEqual(resposta.status_code, 200)

        resposta = self.client.delete(detalhe)
        self.assertEqual(resposta.status_code, 204)

    def test_criar_categoria_pela_api(self):
        resposta = self.client.post(
            reverse("categoria-list"),
            {
                "nome": "Transporte",
                "tipo": "despesa",
                "descricao": "Gastos com transporte",
            },
        )

        self.assertEqual(resposta.status_code, 201)

    def test_criar_lancamento_pela_api(self):
        resposta = self.client.post(
            reverse("lancamento-list"),
            {
                "descricao": "Compra na farmácia",
                "valor": "80.00",
                "tipo": "despesa",
                "data": "2026-11-16",
                "conta": self.conta.id,
                "categoria": self.categoria_despesa.id,
            },
        )

        self.assertEqual(resposta.status_code, 201)

    def test_criar_orcamento_pela_api(self):
        resposta = self.client.post(
            reverse("orcamento-list"),
            {
                "categoria": self.categoria_despesa.id,
                "limite": "600.00",
                "mes": 11,
                "ano": 2026,
            },
        )

        self.assertEqual(resposta.status_code, 201)

    def test_filtrar_lancamentos_por_tipo(self):
        resposta = self.client.get(
            reverse("lancamento-list"),
            {"tipo": "despesa"},
        )

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(len(resposta.data["results"]), 2)

    def test_pesquisar_lancamento_por_descricao(self):
        resposta = self.client.get(
            reverse("lancamento-list"),
            {"search": "mercado"},
        )

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(len(resposta.data["results"]), 1)

    def test_ordenar_lancamentos_por_valor(self):
        resposta = self.client.get(
            reverse("lancamento-list"),
            {"ordering": "-valor"},
        )

        self.assertEqual(resposta.status_code, 200)

        valores = [
            Decimal(item["valor"])
            for item in resposta.data["results"]
        ]

        self.assertEqual(
            valores,
            sorted(valores, reverse=True),
        )

    def test_paginacao_da_api(self):
        resposta = self.client.get(
            reverse("conta-list"),
            {"page_size": 1},
        )

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.data["page_size"], 1)
        self.assertEqual(resposta.data["total_pages"], 1)
        self.assertEqual(len(resposta.data["results"]), 1)

    def test_impedir_page_size_maior_que_100(self):
        resposta = self.client.get(
            reverse("conta-list"),
            {"page_size": 101},
        )

        self.assertEqual(resposta.status_code, 400)


