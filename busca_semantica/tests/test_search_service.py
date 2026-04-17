"""
Testes para o SearchService.
Utiliza mocks para simular embeddings e índice FAISS.
"""
import pytest
import numpy as np
from unittest.mock import MagicMock, patch


class TestSearchService:
    """Testes do serviço de busca semântica."""

    def test_index_documents_returns_count(
        self, mock_sentence_transformer, mock_faiss_index, mock_documents
    ):
        """Verifica se index_documents retorna a quantidade de documentos indexados."""
        from app.services.search_service import SearchService

        service = SearchService()
        count = service.index_documents(mock_documents)

        assert count == len(mock_documents)
        assert len(service) == len(mock_documents)

    def test_search_returns_results(
        self, mock_sentence_transformer, mock_faiss_index, mock_documents
    ):
        """Verifica se search retorna resultados formatados corretamente."""
        from app.services.search_service import SearchService

        service = SearchService()
        service.index_documents(mock_documents)

        results = service.search("Python", top_k=3)

        assert len(results) > 0
        assert "document" in results[0]
        assert "score" in results[0]
        assert isinstance(results[0]["score"], float)

    def test_search_respects_top_k(
        self, mock_sentence_transformer, mock_faiss_index, mock_documents
    ):
        """Verifica se search respeita o parâmetro top_k."""
        from app.services.search_service import SearchService

        service = SearchService()
        service.index_documents(mock_documents)

        results = service.search("teste", top_k=2)

        assert len(results) == 2

    def test_index_from_directory_reads_txt_files(
        self, mock_sentence_transformer, mock_faiss_index, tmp_path
    ):
        """Verifica se index_from_directory lê arquivos .txt corretamente."""
        from app.services.search_service import SearchService

        # Cria diretório temporário com arquivos de teste
        docs_dir = tmp_path / "documents"
        docs_dir.mkdir()

        (docs_dir / "doc1.txt").write_text("Conteudo do documento 1", encoding="utf-8")
        (docs_dir / "doc2.txt").write_text("Conteudo do documento 2", encoding="utf-8")

        service = SearchService()

        with patch("app.services.search_service.settings") as mock_settings:
            mock_settings.documents_path = str(docs_dir)
            count = service.index_from_directory(str(docs_dir))

        assert count == 2

    def test_index_from_directory_raises_when_no_documents(
        self, mock_sentence_transformer, mock_faiss_index, tmp_path
    ):
        """Verifica se index_from_directory lança erro quando não há documentos."""
        from app.services.search_service import SearchService

        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()

        service = SearchService()

        with pytest.raises(ValueError, match="Nenhum documento"):
            service.index_from_directory(str(empty_dir))

    def test_index_from_directory_raises_when_directory_not_found(
        self, mock_sentence_transformer, mock_faiss_index
    ):
        """Verifica se index_from_directory lança erro quando diretório não existe."""
        from app.services.search_service import SearchService

        service = SearchService()

        with pytest.raises(FileNotFoundError):
            service.index_from_directory("/caminho/inexistente")

    def test_save_and_load_index(
        self, mock_sentence_transformer, mock_documents, tmp_path
    ):
        """Verifica se save_index e load_index funcionam corretamente."""
        from app.services.search_service import SearchService

        service = SearchService()
        service.index_documents(mock_documents)

        # Salva em arquivo temporário
        index_path = tmp_path / "test_index"
        service.save_index(str(index_path))

        # Cria novo serviço e carrega
        new_service = SearchService()
        new_service.load_index(str(index_path))

        assert len(new_service) == len(mock_documents)

    def test_index_exists_returns_true_when_files_exist(
        self, mock_sentence_transformer, tmp_path
    ):
        """Verifica se index_exists retorna True quando arquivos existem."""
        from app.services.search_service import SearchService

        service = SearchService()
        index_path = tmp_path / "existing_index"

        # Cria arquivo .faiss fake
        (tmp_path / "existing_index.faiss").write_text("fake")

        with patch("app.services.search_service.settings") as mock_settings:
            mock_settings.faiss_index_path = str(index_path)
            assert service.index_exists(str(index_path)) is True

    def test_index_exists_returns_false_when_files_missing(
        self, mock_sentence_transformer
    ):
        """Verifica se index_exists retorna False quando arquivos não existem."""
        from app.services.search_service import SearchService

        service = SearchService()

        assert service.index_exists("/caminho/inexistente") is False


class TestEmbeddingGenerator:
    """Testes do gerador de embeddings."""

    def test_encode_documents_returns_numpy_array(
        self, mock_sentence_transformer, mock_documents, mock_embedding_dimension
    ):
        """Verifica se encode_documents retorna array numpy."""
        from app.embeddings.generator import EmbeddingGenerator

        generator = EmbeddingGenerator()
        embeddings = generator.encode_documents(mock_documents)

        assert isinstance(embeddings, np.ndarray)
        assert embeddings.shape == (len(mock_documents), mock_embedding_dimension)

    def test_encode_query_returns_numpy_array(
        self, mock_sentence_transformer, mock_embedding_dimension
    ):
        """Verifica se encode_query retorna array numpy."""
        from app.embeddings.generator import EmbeddingGenerator

        generator = EmbeddingGenerator()
        embedding = generator.encode_query("query de teste")

        assert isinstance(embedding, np.ndarray)
        assert embedding.shape == (mock_embedding_dimension,)

    def test_get_embedding_dimension_returns_int(
        self, mock_sentence_transformer, mock_embedding_dimension
    ):
        """Verifica se get_embedding_dimension retorna inteiro."""
        from app.embeddings.generator import EmbeddingGenerator

        generator = EmbeddingGenerator()
        dim = generator.get_embedding_dimension()

        assert isinstance(dim, int)
        assert dim == mock_embedding_dimension


class TestFAISSStore:
    """Testes do armazenamento FAISS."""

    def test_add_documents_updates_count(self, mock_embedding_dimension):
        """Verifica se add_documents atualiza o contador de documentos."""
        from app.vectorstore.faiss_store import FAISSStore

        store = FAISSStore(dimension=mock_embedding_dimension)
        embeddings = np.random.randn(3, mock_embedding_dimension).astype(np.float32)
        documents = ["doc1", "doc2", "doc3"]

        store.add_documents(embeddings, documents)

        assert len(store) == 3

    def test_search_returns_formatted_results(
        self, mock_embedding_dimension, mock_documents
    ):
        """Verifica se search retorna resultados no formato esperado."""
        from app.vectorstore.faiss_store import FAISSStore

        store = FAISSStore(dimension=mock_embedding_dimension)

        # Adiciona documentos
        embeddings = np.random.randn(3, mock_embedding_dimension).astype(np.float32)
        store.add_documents(embeddings, mock_documents[:3])

        # Busca
        query = np.random.randn(mock_embedding_dimension).astype(np.float32)
        results = store.search(query, top_k=2)

        assert len(results) == 2
        assert "document" in results[0]
        assert "score" in results[0]

    def test_save_and_load_preserves_documents(
        self, mock_embedding_dimension, mock_documents, tmp_path
    ):
        """Verifica se save e load preservam os documentos."""
        from app.vectorstore.faiss_store import FAISSStore

        store = FAISSStore(dimension=mock_embedding_dimension)
        embeddings = np.random.randn(3, mock_embedding_dimension).astype(np.float32)
        store.add_documents(embeddings, mock_documents[:3])

        # Salva
        path = tmp_path / "test_store"
        store.save(str(path))

        # Carrega em novo store
        new_store = FAISSStore(dimension=mock_embedding_dimension)
        new_store.load(str(path))

        assert len(new_store) == 3
