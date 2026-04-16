"""
Ponto de entrada da aplicação FastAPI.
Configura a aplicação e registra os routers.
"""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.v1.books import router as books_router
from app.core.config import settings
from app.core.database import Base, engine

# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Inicializa a aplicação FastAPI
app = FastAPI(
    title=settings.app_name,
    description="API para cadastro e consulta de livros",
    version="1.0.0"
)


# Exception handler global para erros não tratados
# FastAPI já trata exceções automaticamente (retorna 500)
# Pydantic retorna 422 para dados inválidos
# HTTPException para erros controlados (404, 400, etc.)
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Captura exceções não tratadas e retorna resposta padronizada."""
    return JSONResponse(
        status_code=500,
        content={"detail": "Erro interno do servidor", "error": str(exc)}
    )


# Registra o router de livros com prefixo de versionamento
app.include_router(books_router, prefix="/api/v1")
