"""
Endpoints da API de livros.
Recebe requisições HTTP, valida entrada e delega para o service.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.book import BookCreate, BookResponse
from app.services.book_service import BookService

# Cria router com prefixo e tag para documentação
router = APIRouter(prefix="/books", tags=["Livros"])


# POST /books - Cadastra um novo livro
@router.post("/", response_model=BookResponse, status_code=201)
def create_book(book_data: BookCreate, db: Session = Depends(get_db)):
    """Cadastra um novo livro na biblioteca."""
    service = BookService(db)
    return service.create_book(book_data)


# GET /books/search/titulo - Consulta livros por título
@router.get("/search/titulo", response_model=list[BookResponse])
def search_by_titulo(
    titulo: str = Query(..., min_length=1, description="Título do livro"),
    skip: int = Query(0, ge=0, description="Registros a pular"),
    limit: int = Query(20, ge=1, le=100, description="Máximo de registros"),
    db: Session = Depends(get_db)
):
    """Consulta livros por título com paginação."""
    service = BookService(db)
    return service.search_by_titulo(titulo, skip, limit)


# GET /books/search/autor - Consulta livros por autor
@router.get("/search/autor", response_model=list[BookResponse])
def search_by_autor(
    autor: str = Query(..., min_length=1, description="Nome do autor"),
    skip: int = Query(0, ge=0, description="Registros a pular"),
    limit: int = Query(20, ge=1, le=100, description="Máximo de registros"),
    db: Session = Depends(get_db)
):
    """Consulta livros por autor com paginação."""
    service = BookService(db)
    return service.search_by_autor(autor, skip, limit)
