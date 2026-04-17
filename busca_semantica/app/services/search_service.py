"""
Serviço de busca semântica.
Orquestra geração de embeddings e busca no FAISS.
"""
import os
from pathlib import Path

from app.core.config import settings
from app.embeddings.generator import EmbeddingGenerator
from app.vectorstore.faiss_store import FAISSStore


class SearchService:
    """
    Serviço que gerencia indexação e busca de documentos.
    Combina EmbeddingGenerator + FAISSStore.
    """

    def __init__(self):
        self.generator = EmbeddingGenerator()
        self.store = FAISSStore(dimension=self.generator.get_embedding_dimension())

    def index_documents(self, documents: list[str]) -> int:
        """
        Indexa uma lista de documentos.

        Args:
            documents: Lista de textos para indexar

        Returns:
            Número de documentos indexados
        """
        # Gera embeddings para todos os documentos
        embeddings = self.generator.encode_documents(documents)

        # Adiciona ao índice FAISS
        self.store.add_documents(embeddings, documents)

        return len(documents)

    def index_from_directory(self, directory: str = None) -> int:
        """
        Indexa todos os arquivos .txt de um diretório.

        Args:
            directory: Caminho do diretório (usa config se não especificado)

        Returns:
            Número de documentos indexados
        """
        if directory is None:
            directory = settings.documents_path

        documents = []
        path = Path(directory)

        if not path.exists():
            raise FileNotFoundError(f"Diretório não encontrado: {directory}")

        # Lê todos os arquivos .txt do diretório
        for file_path in path.glob("*.txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    documents.append(content)

        if not documents:
            raise ValueError(f"Nenhum documento .txt encontrado em: {directory}")

        return self.index_documents(documents)

    def search(self, query: str, top_k: int = None) -> list[dict]:
        """
        Busca documentos similares à query.

        Args:
            query: Texto da busca
            top_k: Número de resultados (usa config se não especificado)

        Returns:
            Lista de dicts com 'document' e 'score'
        """
        # Gera embedding da query
        query_embedding = self.generator.encode_query(query)

        # Busca no FAISS
        results = self.store.search(query_embedding, top_k)

        return results

    def save_index(self, path: str = None) -> None:
        """Salva o índice em disco."""
        self.store.save(path)

    def load_index(self, path: str = None) -> None:
        """Carrega o índice do disco."""
        self.store.load(path)

    def index_exists(self, path: str = None) -> bool:
        """Verifica se o índice existe em disco."""
        if path is None:
            path = settings.faiss_index_path
        return os.path.exists(f"{path}.faiss")

    def __len__(self) -> int:
        """Retorna o número de documentos indexados."""
        return len(self.store)
