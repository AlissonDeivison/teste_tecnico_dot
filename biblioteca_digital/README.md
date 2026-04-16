# Biblioteca Digital API

API REST para cadastro e consulta de livros em uma biblioteca virtual.

## Desafio

Desenvolver uma API que permita:

1. Cadastro de livros com: título, autor, data de publicação e resumo
2. Consulta de livros por título ou autor
3. Endpoints documentados
4. Banco de dados SQLite
5. Testes unitários

## Stack

- FastAPI
- SQLAlchemy (ORM)
- SQLite
- Pytest

## Arquitetura

Projeto estruturado em camadas seguindo Clean Architecture:

```
app/
├── api/v1/          # Endpoints (Presentation Layer)
├── services/        # Regras de negócio (Business Layer)
├── repositories/    # Acesso a dados (Data Layer)
├── models/          # Entidades ORM
├── schemas/         # DTOs Pydantic (validação entrada/saída)
└── core/            # Configurações e database
```

### Camadas

**API (Presentation)**: Recebe requisições HTTP, valida entrada via schemas, delega para services.

**Services (Business)**: Contém regras de negócio. Orquestra repositories e retorna dados para API.

**Repositories (Data)**: Abstrai operações de banco. Facilita testes e troca de banco de dados.

**Models**: Entidades SQLAlchemy mapeadas para tabelas.

**Schemas**: Modelos Pydantic para validação e serialização de requests/responses.

### Benefícios

- Separação de responsabilidades
- Testabilidade (mocks em cada camada)
- Baixo acoplamento entre camadas

## Instalação

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

## Executando o Servidor

```bash
# Iniciar servidor de desenvolvimento
uvicorn app.main:app --reload

# Servidor inicia em http://localhost:8000
```

### Documentação da API

Após iniciar o servidor, acesse:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/api/v1/books/` | Cadastra um livro |
| GET | `/api/v1/books/search/titulo?titulo=x` | Busca por título |
| GET | `/api/v1/books/search/autor?autor=x` | Busca por autor |

### Exemplo de Requisição

```bash
# Cadastrar livro
curl -X POST http://localhost:8000/api/v1/books/ \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "O Avesso da Pele",
    "autor": "Jeferson Tenório",
    "data_publicacao": "2020-08-20",
    "resumo": "Uma narrativa sobre identidade e racismo no Brasil"
  }'

# Buscar por título
curl "http://localhost:8000/api/v1/books/search/titulo?titulo=Avesso"

# Buscar por autor
curl "http://localhost:8000/api/v1/books/search/autor?autor=Jeferson"
```

## Testes

```bash
# Rodar todos os testes
pytest

# Rodar com output detalhado
pytest -v

# Rodar apenas testes de integração
pytest tests/integration/ -v

# Rodar com cobertura (requer pytest-cov)
pytest --cov=app tests/
```

### Estrutura de Testes

```
tests/
├── conftest.py      # Fixtures compartilhadas
├── integration/     # Testes de fluxo completo
│   └── test_books_api.py
└── unit/            # Testes isolados por camada
```
