
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Conta, Categoria, Lancamento, Orcamento


class FinanceiroAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.conta = Conta.objects.create(
            nome="Conta Teste",
            banco="Nubank",
            saldo_inicial=1000
        )

        self.categoria_despesa = Categoria.objects.create(
            nome="Alimentação",
            tipo="despesa"
        )

        self.categoria_receita = Categoria.objects.create(
            nome="Salário",
            tipo="receita"
        )

    def test_listar_contas(self):
        resposta = self.client.get("/api/financeiro/contas/")
        self.assertEqual(resposta.status_code, 200)

    def test_criar_conta(self):
        dados = {
            "nome": "Conta Nova",
            "banco": "Inter",
            "saldo_inicial": "500.00",
            "ativa": True
        }

        resposta = self.client.post(
            "/api/financeiro/contas/", dados
        )

        self.assertEqual(resposta.status_code, 201)
        self.assertTrue(
            Conta.objects.filter(nome="Conta Nova").exists()
        )

    def test_impedir_saldo_negativo(self):
        dados = {
            "nome": "Conta Inválida",
            "banco": "Teste",
            "saldo_inicial": "-100.00",
            "ativa": True
        }

        resposta = self.client.post(
            "/api/financeiro/contas/", dados
        )

        self.assertEqual(resposta.status_code, 400)

    def test_impedir_lancamento_com_valor_negativo(self):
        dados = {
            "descricao": "Compra",
            "valor": "-50.00",
            "tipo": "despesa",
            "data": "2026-11-12",
            "conta": self.conta.id,
            "categoria": self.categoria_despesa.id
        }

        resposta = self.client.post(
            "/api/financeiro/lancamentos/", dados
        )

        self.assertEqual(resposta.status_code, 400)

    def test_impedir_categoria_com_tipo_diferente(self):
        dados = {
            "descricao": "Compra de roupa",
            "valor": "50.00",
            "tipo": "despesa",
            "data": "2026-11-12",
            "conta": self.conta.id,
            "categoria": self.categoria_receita.id
        }

        resposta = self.client.post(
            "/api/financeiro/lancamentos/", dados
        )

        self.assertEqual(resposta.status_code, 400)

    def test_impedir_orcamento_em_categoria_de_receita(self):
        dados = {
            "categoria": self.categoria_receita.id,
            "limite": "500.00",
            "mes": 11,
            "ano": 2026
        }

        resposta = self.client.post(
            "/api/financeiro/orcamentos/", dados
        )

        self.assertEqual(resposta.status_code, 400)

    def test_criar_orcamento(self):
        dados = {
            "categoria": self.categoria_despesa.id,
            "limite": "500.00",
            "mes": 11,
            "ano": 2026
        }

        resposta = self.client.post(
            "/api/financeiro/orcamentos/", dados
        )

        self.assertEqual(resposta.status_code, 201)
