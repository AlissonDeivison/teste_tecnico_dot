"""
Configurações centralizadas da aplicação.
Usa pydantic-settings para validação e suporte a variáveis de ambiente.
"""
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Configurações da aplicação."""
    app_name: str = "Biblioteca Digital API"  # Nome exibido na documentação
    database_url: str = "sqlite:///./biblioteca.db"  # URL de conexão com o banco

    class Config:
        env_file = ".env"  # Permite sobrescrever valores via arquivo .env


# Instância única de configurações (singleton)
settings = Settings()
