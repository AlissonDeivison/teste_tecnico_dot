"""
Configurações e fixtures compartilhadas para os testes.
Usa mocks para evitar download real do modelo de embeddings.
"""
import sys
from pathlib import Path

# Adiciona o diretório raiz do projeto ao path do Python
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
import numpy as np
from unittest.mock import MagicMock, patch


@pytest.fixture
def mock_embedding_dimension():
    """Retorna a dimensão dos embeddings do modelo mockado."""
    return 384


@pytest.fixture
def mock_embeddings():
    """
    Fixture que retorna embeddings simulados para testes.
    Gera vetores normalizados aleatórios.
    """
    def _generate(count=5, dim=384):
        # Gera vetores aleatórios e normaliza
        vectors = np.random.randn(count, dim).astype(np.float32)
        # Normaliza para similaridade por cosseno
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        return vectors / norms
    return _generate


@pytest.fixture
def mock_documents():
    """Retorna documentos de exemplo para testes."""
    return [
        "Python é uma linguagem de programação versátil.",
        "JavaScript é usado principalmente para desenvolvimento web.",
        "Machine learning é uma subárea da inteligência artificial.",
        "Bancos de dados vetoriais armazenam embeddings.",
        "FAISS é uma biblioteca de busca por similaridade.",
    ]


@pytest.fixture
def mock_sentence_transformer(mock_embedding_dimension):
    """
    Fixture que mocka o SentenceTransformer.
    Evita download real do modelo durante os testes.
    """
    with patch("app.embeddings.generator.SentenceTransformer") as mock_class:
        mock_instance = MagicMock()

        # Configura o método encode para retornar vetores mockados
        def mock_encode(texts, convert_to_numpy=True):
            is_single_string = isinstance(texts, str)
            if is_single_string:
                texts = [texts]
            count = len(texts)
            # Gera embeddings determinísticos
            np.random.seed(42)
            vectors = np.random.randn(count, mock_embedding_dimension).astype(np.float32)
            norms = np.linalg.norm(vectors, axis=1, keepdims=True)
            result = (vectors / norms) if convert_to_numpy else vectors
            # Retorna vetor 1D se input foi string única
            return result[0] if is_single_string else result

        mock_instance.encode.side_effect = mock_encode
        mock_instance.get_embedding_dimension.return_value = mock_embedding_dimension

        mock_class.return_value = mock_instance
        yield mock_class


@pytest.fixture
def mock_faiss_index():
    """
    Fixture que mocka o índice FAISS.
    """
    with patch("app.vectorstore.faiss_store.faiss.IndexFlatIP") as mock_class:
        mock_instance = MagicMock()
        mock_instance.ntotal = 0

        # Simula adição de vetores
        def mock_add(vectors):
            mock_instance.ntotal += len(vectors)

        mock_instance.add.side_effect = mock_add

        # Simula busca - retorna índices e scores mockados
        def mock_search(query, k):
            count = min(k, mock_instance.ntotal) if mock_instance.ntotal > 0 else k
            # Retorna índices sequenciais e scores decrescentes
            indices = np.array([list(range(count))], dtype=np.int64)
            scores = np.array([[0.95 - i * 0.1 for i in range(count)]], dtype=np.float32)
            return scores, indices

        mock_instance.search.side_effect = mock_search
        mock_class.return_value = mock_instance
        yield mock_class


@pytest.fixture
def mock_settings(mock_embedding_dimension):
    """
    Fixture que mocka as configurações para testes.
    Evita necessidade de .env real durante os testes.
    """
    with patch("app.core.config.settings") as mock:
        mock.embedding_model = "sentence-transformers/all-MiniLM-L6-v2"
        mock.faiss_index_path = "data/test_faiss_index"
        mock.documents_path = "data/test_documents"
        mock.top_k = 3
        yield mock
