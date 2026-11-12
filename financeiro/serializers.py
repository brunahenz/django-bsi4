
from rest_framework import serializers
from .models import Conta, Categoria, Lancamento, Orcamento


class ContaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conta
        fields = '__all__'


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'


class LancamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lancamento
        fields = '__all__'

    def validate(self, dados):
        categoria = dados.get(
            'categoria',
            self.instance.categoria if self.instance else None
        )
        tipo = dados.get(
            'tipo',
            self.instance.tipo if self.instance else None
        )

        if categoria and tipo and categoria.tipo != tipo:
            raise serializers.ValidationError({
                'categoria': 'O tipo da categoria deve corresponder ao tipo do lançamento.'
            })

        return dados


class OrcamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orcamento
        fields = '__all__'

    def validate(self, dados):
        categoria = dados.get(
            'categoria',
            self.instance.categoria if self.instance else None
        )
        mes = dados.get(
            'mes',
            self.instance.mes if self.instance else None
        )
        ano = dados.get(
            'ano',
            self.instance.ano if self.instance else None
        )

        if categoria and categoria.tipo != 'despesa':
            raise serializers.ValidationError({
                'categoria': 'O orçamento deve estar associado a uma categoria de despesa.'
            })

        if mes is not None and not 1 <= mes <= 12:
            raise serializers.ValidationError({
                'mes': 'O mês deve estar entre 1 e 12.'
            })

        if ano is not None and not 2000 <= ano <= 2100:
            raise serializers.ValidationError({
                'ano': 'Informe um ano entre 2000 e 2100.'
            })

        return dados
