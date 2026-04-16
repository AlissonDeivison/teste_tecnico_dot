"""
Service de livros: contém regras de negócio.
Orquestra o repository e pode adicionar validações extras.
"""
from sqlalchemy.orm import Session

from app.models.book import Book
from app.repositories.book_repo import BookRepository
from app.schemas.book import BookCreate


class BookService:
    """Regras de negócio para operações com livros."""

    def __init__(self, db: Session):
        self.repository = BookRepository(db)

    # Recebe BookCreate (schema) e retorna Book (model)
    def create_book(self, book_data: BookCreate) -> Book:
        """Cadastra um novo livro."""
        return self.repository.create(book_data)

    # Recebe titulo (str), skip e limit (int) e retorna lista de Book
    def search_by_titulo(self, titulo: str, skip: int = 0, limit: int = 20) -> list[Book]:
        """Consulta livros por título com paginação."""
        return self.repository.search_by_titulo(titulo, skip, limit)

    # Recebe autor (str), skip e limit (int) e retorna lista de Book
    def search_by_autor(self, autor: str, skip: int = 0, limit: int = 20) -> list[Book]:
        """Consulta livros por autor com paginação."""
        return self.repository.search_by_autor(autor, skip, limit)
