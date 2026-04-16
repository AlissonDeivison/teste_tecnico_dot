"""
Schemas Pydantic para validação e serialização de livros.
Separa a representação da API do modelo de banco de dados.
"""
from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


# Schema base com campos comuns
class BookBase(BaseModel):
    titulo: str = Field(..., min_length=1, max_length=255)
    autor: str = Field(..., min_length=1, max_length=255)
    data_publicacao: date
    resumo: Optional[str] = None


# Schema para criação (entrada da API)
class BookCreate(BookBase):
    """Dados necessários para criar um livro."""
    pass


# Schema para resposta (saída da API)
class BookResponse(BookBase):
    """Dados retornados pela API, inclui o ID."""
    id: str

    class Config:
        from_attributes = True  # Permite conversão de ORM para Pydantic


# Schema para atualização parcial
class BookUpdate(BaseModel):
    """Campos opcionais para atualização parcial (PATCH)."""
    titulo: Optional[str] = Field(None, min_length=1, max_length=255)
    autor: Optional[str] = Field(None, min_length=1, max_length=255)
    data_publicacao: Optional[date] = None
    resumo: Optional[str] = None
