"""
Configurações centralizadas da aplicação.
Usa pydantic-settings para carregar a API key do arquivo .env.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configurações do chatbot."""
    openai_api_key: str  # Chave da API OpenAI (obrigatória)
    openai_model: str = "gpt-4"  # Modelo padrão, pode ser alterado via .env

    model_config = SettingsConfigDict(env_file=".env")


# Instância única de configurações (singleton)
settings = Settings()
