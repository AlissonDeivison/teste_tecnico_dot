"""
Gerador de embeddings usando sentence-transformers.
Encapsula o modelo e fornece métodos para gerar vetores de texto.
"""
import numpy as np
from sentence_transformers import SentenceTransformer

from app.core.config import settings


class EmbeddingGenerator:
    """
    Gera embeddings de texto usando modelo da Hugging Face.
    Usa API assimétrica: encode_query() para buscas, encode_document() para docs.
    """

    def __init__(self):
        # Carrega o modelo na inicialização (download automático no primeiro uso)
        self.model = SentenceTransformer(settings.embedding_model)

    def encode_documents(self, documents: list[str]) -> np.ndarray:
        """
        Gera embeddings para uma lista de documentos.
        Usa encode_document() otimizado para indexação.
        """
        return self.model.encode_document(documents)

    def encode_query(self, query: str) -> np.ndarray:
        """
        Gera embedding para uma query de busca.
        Usa encode_query() otimizado para recuperação.
        """
        return self.model.encode_query(query)

    def get_embedding_dimension(self) -> int:
        """Retorna a dimensão dos embeddings gerados pelo modelo."""
        return self.model.get_sentence_embedding_dimension()
