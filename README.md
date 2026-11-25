# Meu Financeiro

## Sobre o projeto

O Meu Financeiro é uma aplicação web desenvolvida como projeto final da disciplina de Desenvolvimento Web.

O objetivo é ajudar no controle financeiro, permitindo cadastrar contas, organizar categorias, registrar receitas e despesas e acompanhar orçamentos.

O projeto foi desenvolvido utilizando Python, Django e Django REST Framework, com uma API REST para gerenciar os dados.

## Tecnologias utilizadas

- Python
- Django
- Django REST Framework
- SQLite
- Django Filter
- drf-spectacular (Swagger)
- HTML e CSS

## Funcionalidades

- Cadastro, consulta, atualização e exclusão de contas.
- Cadastro e gerenciamento de categorias de receitas e despesas.
- Registro de receitas e despesas.
- Associação de lançamentos com contas e categorias.
- Cadastro de orçamentos por categoria, mês e ano.
- Consulta dos dados por filtros.
- Busca textual.
- Ordenação dos resultados.
- Paginação da API.
- Dashboard com resumo financeiro.

## Models do projeto

O projeto possui quatro models principais:

**Conta:** armazena o nome da conta, banco, saldo inicial e situação (ativa ou inativa).

**Categoria:** organiza os lançamentos em categorias de receita ou despesa.

**Lancamento:** registra receitas e despesas, contendo descrição, valor, data, conta, categoria e observação.

**Orcamento:** permite definir um limite de gastos para uma categoria de despesa em determinado mês e ano.

## Regras de negócio e validações

O sistema possui algumas validações para manter os dados consistentes:

- Não permite saldo inicial negativo.
- Não permite lançamentos com valores negativos ou iguais a zero.
- A categoria precisa corresponder ao tipo do lançamento.
- Um orçamento deve estar associado a uma categoria de despesa.
- O mês do orçamento deve estar entre 1 e 12.
- O ano do orçamento deve estar entre 2000 e 2100.
- Contas e categorias utilizadas em outros registros não podem ser excluídas.

## Como executar o projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/brunahenz/django-bsi4.git
```

### 2. Entrar na pasta

```bash
cd django-bsi4
```

### 3. Instalar as dependências

```bash
uv sync
```

### 4. Aplicar as migrations

```bash
uv run python manage.py migrate
```

### 5. Executar o servidor

```bash
uv run python manage.py runserver
```

A aplicação estará disponível em:

http://127.0.0.1:8000/

## Páginas da aplicação

- `/` - Dashboard principal.
- `/contas/` - Gerenciamento de contas.
- `/categorias/` - Gerenciamento de categorias.
- `/lancamentos/` - Gerenciamento de receitas e despesas.
- `/orcamentos/` - Gerenciamento de orçamentos.

## Documentação da API

A documentação interativa da API está disponível pelo Swagger:

http://127.0.0.1:8000/api/docs/

Também é possível acessar a documentação pelo ReDoc:

http://127.0.0.1:8000/api/redoc/

## Endpoints principais

Todos os recursos possuem operações de CRUD.

| Recurso | Endpoint |
|---|---|
| Contas | `/api/financeiro/contas/` |
| Categorias | `/api/financeiro/categorias/` |
| Lançamentos | `/api/financeiro/lancamentos/` |
| Orçamentos | `/api/financeiro/orcamentos/` |

### Métodos HTTP

- GET: consulta os registros.
- POST: cadastra um novo registro.
- PUT: atualiza completamente um registro.
- DELETE: exclui um registro.

Para consultar um registro específico, basta informar seu ID no final do endpoint.

Exemplo:

`/api/financeiro/contas/1/`

## Filtros, busca, ordenação e paginação

A API permite realizar consultas utilizando parâmetros na URL.

**Filtros:**

```text
/api/financeiro/lancamentos/?tipo=despesa
```

**Busca textual:**

```text
/api/financeiro/lancamentos/?search=mercado
```

**Ordenação:**

```text
/api/financeiro/lancamentos/?ordering=-valor
```

O sinal de menos indica ordem decrescente.

**Paginação:**

```text
/api/financeiro/lancamentos/?page=1&page_size=5
```

O tamanho máximo permitido por página é de 100 registros.

## Banco de dados

O projeto utiliza SQLite para armazenar os dados e o ORM do Django para realizar as operações no banco.

As migrations são utilizadas para criar e atualizar a estrutura das tabelas.

## Testes

Os testes automatizados podem ser executados com o comando:

```bash
uv run python manage.py test financeiro
```
