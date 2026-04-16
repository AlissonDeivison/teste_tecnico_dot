"""
Fixtures compartilhadas para os testes.
Configura banco de dados isolado e cliente de teste.

Fixture: função que prepara dados/recursos antes do teste e limpa depois.
O pytest detecta automaticamente este arquivo e disponibiliza as fixtures.
"""
import pytest
from fastapi.testclient import TestClient  # Cliente HTTP para testar endpoints
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base, get_db
from app.main import app

# Banco SQLite separado para testes (não usa o banco real)
# Isso garante que os testes não afetam dados de produção
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Cria conexão com o banco de testes
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # Necessário para SQLite
)

# Fábrica de sessões para o banco de testes
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# @pytest.fixture: marca a função como fixture (recurso reutilizável)
# scope="function": executa antes/depois de CADA teste (isolamento total)
@pytest.fixture(scope="function")
def db_session():
    """
    Cria sessão de banco limpa para cada teste.

    Fluxo:
    1. Cria todas as tabelas (create_all)
    2. Cria sessão do banco
    3. yield: "pausa" e entrega a sessão para o teste usar
    4. Após o teste: fecha sessão e destrói tabelas (drop_all)

    Isso garante que cada teste começa com banco vazio.
    """
    Base.metadata.create_all(bind=engine)  # Cria tabelas
    session = TestingSessionLocal()
    try:
        yield session  # Entrega sessão para o teste
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)  # Limpa tabelas após teste


@pytest.fixture(scope="function")
def client(db_session):
    """
    Cliente HTTP para testar endpoints.

    Usa dependency_overrides para substituir o banco real pelo de testes.
    Isso faz com que os endpoints usem db_session ao invés do banco real.
    """
    # Função que substitui get_db() original
    def override_get_db():
        try:
            yield db_session  # Usa a sessão de teste
        finally:
            pass

    # Substitui a dependência get_db pela nossa versão de teste
    app.dependency_overrides[get_db] = override_get_db

    # Cria cliente de teste e entrega para o teste usar
    with TestClient(app) as test_client:
        yield test_client

    # Limpa as substituições após o teste
    app.dependency_overrides.clear()
