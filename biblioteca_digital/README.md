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

## Testes

```
tests/
├── unit/           # Testes isolados por camada
└── integration/    # Testes de fluxo completo
```

## Execução

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Documentação disponível em `/docs` (Swagger) e `/redoc`.
