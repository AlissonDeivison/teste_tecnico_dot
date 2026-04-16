"""
Repository de livros: abstrai operações de banco de dados.
Facilita testes e permite trocar o banco sem alterar a lógica de negócio.
"""
from typing import Optional

from sqlalchemy.orm import Session

from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate


class BookRepository:
    """Operações de persistência para a entidade Book."""

    def __init__(self, db: Session):
        self.db = db

    # Recebe BookCreate (schema) e retorna Book (model)
    def create(self, book_data: BookCreate) -> Book:
        """Cria um novo livro no banco."""
        # Converte schema Pydantic para dict e desempacota como kwargs do model
        book = Book(**book_data.model_dump())
        self.db.add(book)
        self.db.commit()
        self.db.refresh(book)  # Atualiza com dados gerados (id)
        return book

    # Recebe book_id (str) e retorna Book ou None
    def get_by_id(self, book_id: str) -> Optional[Book]:
        """Busca livro por ID."""
        return self.db.query(Book).filter(Book.id == book_id).first()

    # Recebe skip e limit (int) e retorna lista de Book
    def get_all(self, skip: int = 0, limit: int = 100) -> list[Book]:
        """Lista todos os livros com paginação."""
        return self.db.query(Book).offset(skip).limit(limit).all()

    # Recebe titulo (str) e retorna lista de Book
    def search_by_titulo(self, titulo: str) -> list[Book]:
        """Busca livros por título (contém)."""
        return self.db.query(Book).filter(Book.titulo.ilike(f"%{titulo}%")).all()

    # Recebe autor (str) e retorna lista de Book
    def search_by_autor(self, autor: str) -> list[Book]:
        """Busca livros por autor (contém)."""
        return self.db.query(Book).filter(Book.autor.ilike(f"%{autor}%")).all()

    # Recebe Book (model) e BookUpdate (schema) e retorna Book atualizado
    def update(self, book: Book, book_data: BookUpdate) -> Book:
        """Atualiza campos do livro."""
        update_data = book_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(book, field, value)
        self.db.commit()
        self.db.refresh(book)
        return book

    # Recebe Book (model) e não retorna nada (None)
    def delete(self, book: Book) -> None:
        """Remove livro do banco."""
        self.db.delete(book)
        self.db.commit()
