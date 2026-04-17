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
    Usa sentence-transformers para codificação de textos.
    """

    def __init__(self):
        # Carrega o modelo na inicialização (download automático no primeiro uso)
        self.model = SentenceTransformer(settings.embedding_model)

    def encode_documents(self, documents: list[str]) -> np.ndarray:
        """
        Gera embeddings para uma lista de documentos.
        """
        return self.model.encode(documents, convert_to_numpy=True)

    def encode_query(self, query: str) -> np.ndarray:
        """
        Gera embedding para uma query de busca.
        """
        return self.model.encode(query, convert_to_numpy=True)

    def get_embedding_dimension(self) -> int:
        """Retorna a dimensão dos embeddings gerados pelo modelo."""
        return self.model.get_embedding_dimension()
