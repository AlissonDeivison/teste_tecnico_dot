"""
Armazenamento de vetores usando FAISS.
Gerencia o índice para busca por similaridade.
"""
import os
import numpy as np
import faiss

from app.core.config import settings


class FAISSStore:
    """
    Gerencia o índice FAISS para busca por similaridade vetorial.
    Usa IndexFlatIP (Inner Product) para similaridade por cosseno.
    """

    def __init__(self, dimension: int):
        """
        Inicializa o índice FAISS.

        Args:
            dimension: Dimensão dos vetores (768 para embeddinggemma-300m)
        """
        self.dimension = dimension
        # IndexFlatIP usa produto interno (equivalente a cosseno para vetores normalizados)
        self.index = faiss.IndexFlatIP(dimension)
        # Lista para mapear índice FAISS -> documento original
        self.documents: list[str] = []

    def add_documents(self, embeddings: np.ndarray, documents: list[str]) -> None:
        """
        Adiciona embeddings e documentos ao índice.

        Args:
            embeddings: Array de embeddings (n_docs x dimension)
            documents: Lista de textos originais dos documentos
        """
        # Normaliza vetores para usar produto interno como similaridade cosseno
        faiss.normalize_L2(embeddings)
        self.index.add(embeddings)
        self.documents.extend(documents)

    def search(self, query_embedding: np.ndarray, top_k: int = None) -> list[dict]:
        """
        Busca os documentos mais similares à query.

        Args:
            query_embedding: Embedding da query de busca
            top_k: Número de resultados (usa config se não especificado)

        Returns:
            Lista de dicts com 'document' e 'score'
        """
        if top_k is None:
            top_k = settings.top_k

        # Normaliza query para similaridade cosseno
        query_embedding = query_embedding.reshape(1, -1).astype(np.float32)
        faiss.normalize_L2(query_embedding)

        # Busca os top_k mais similares
        scores, indices = self.index.search(query_embedding, top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx != -1:  # -1 indica resultado inválido
                results.append({
                    "document": self.documents[idx],
                    "score": float(score),
                })

        return results

    def save(self, path: str = None) -> None:
        """
        Salva o índice FAISS em disco.

        Args:
            path: Caminho do arquivo (usa config se não especificado)
        """
        if path is None:
            path = settings.faiss_index_path

        os.makedirs(os.path.dirname(path), exist_ok=True)
        faiss.write_index(self.index, f"{path}.faiss")

        # Salva documentos separadamente
        with open(f"{path}.docs", "w", encoding="utf-8") as f:
            for doc in self.documents:
                f.write(doc.replace("\n", "\\n") + "\n")

    def load(self, path: str = None) -> None:
        """
        Carrega o índice FAISS do disco.

        Args:
            path: Caminho do arquivo (usa config se não especificado)
        """
        if path is None:
            path = settings.faiss_index_path

        self.index = faiss.read_index(f"{path}.faiss")

        # Carrega documentos
        with open(f"{path}.docs", "r", encoding="utf-8") as f:
            self.documents = [line.strip().replace("\\n", "\n") for line in f]

    def __len__(self) -> int:
        """Retorna o número de documentos no índice."""
        return self.index.ntotal
