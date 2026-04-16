"""
SQLAlchemy: ORM mais maduro do ecossistema Python.
Facilita troca de banco (SQLite -> PostgreSQL) sem alterar código da aplicação.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Cria conexão com o banco SQLite
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False}  # Necessário para SQLite
)

# Fábrica de sessões do banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe base para os models
Base = declarative_base()

# Gerenciador de sessão do banco para injeção de dependência
def get_db():
    """Dependency injection para injetar sessão do banco nos endpoints."""
    db = SessionLocal()
    try:
        yield db  # Retorna sessão para o endpoint
    finally:
        db.close()  # Garante fechamento mesmo em caso de erro
