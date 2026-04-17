"""
Configurações e fixtures compartilhadas para os testes.
Usa mocks para evitar chamadas reais à API da OpenAI.
"""
import sys
from pathlib import Path

# Adiciona o diretório raiz do projeto ao path do Python
# Permite importar módulos como 'app.services.chat_service'
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from unittest.mock import MagicMock, patch


@pytest.fixture
def mock_llm_response():
    """
    Mock da resposta do LLM.
    Retorna um objeto que simula a resposta do ChatOpenAI.
    """
    mock_response = MagicMock()
    mock_response.content = "Esta é uma resposta simulada do assistente."
    return mock_response


@pytest.fixture
def mock_chat_openai(mock_llm_response):
    """
    Fixture que mocka o ChatOpenAI para evitar chamadas à API.
    Usa patch para substituir a classe durante os testes.
    """
    with patch("app.llm.client.ChatOpenAI") as mock_class:
        # Configura o mock para retornar a resposta simulada
        mock_instance = MagicMock()
        mock_instance.invoke.return_value = mock_llm_response
        mock_class.return_value = mock_instance
        yield mock_class


@pytest.fixture
def mock_settings():
    """
    Fixture que mocka as configurações para testes.
    Evita necessidade de .env real durante os testes.
    """
    with patch("app.core.config.settings") as mock:
        mock.openai_api_key = "sk-test-key-fake"
        mock.openai_model = "gpt-4"
        yield mock
