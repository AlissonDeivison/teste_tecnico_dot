"""
Configurações centralizadas da aplicação.
Define modelo de embeddings e caminhos de armazenamento.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configurações do sistema de busca semântica."""

    # Modelo de embeddings da Hugging Face (sentence-transformers)
    # google/embeddinggemma-300m: modelo recente do Google DeepMind
    # - 768 dimensões, suporte a 100+ idiomas
    # - API assimétrica: encode_query() para buscas, encode_document() para docs
    embedding_model: str = "google/embeddinggemma-300m"

    # Caminho para salvar o índice FAISS
    faiss_index_path: str = "data/faiss_index"

    # Caminho para os documentos de texto
    documents_path: str = "data/documents"

    # Número de resultados retornados na busca
    top_k: int = 5

    model_config = SettingsConfigDict(env_file=".env")


# Instância única de configurações (singleton)
settings = Settings()
