"""
Model Book: representa a tabela de livros no banco de dados.
"""
import uuid

from sqlalchemy import Column, String, Date, Text
from sqlalchemy.dialects.sqlite import CHAR

from app.core.database import Base


class Book(Base):
    """Entidade Livro mapeada para tabela 'books'."""
    __tablename__ = "books"

    # UUID como chave primária, gerado automaticamente
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    titulo = Column(String(255), nullable=False, index=True)  # Indexado para busca
    autor = Column(String(255), nullable=False, index=True)  # Indexado para busca
    data_publicacao = Column(Date, nullable=False)
    resumo = Column(Text, nullable=True)
