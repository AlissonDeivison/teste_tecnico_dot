"""
Testes para o ChatService.
Utiliza mocks para simular respostas do LLM sem chamar a API real.
"""
import pytest
from unittest.mock import MagicMock, patch
from langchain_core.messages import HumanMessage, AIMessage


class TestChatService:
    """Testes do serviço de chat."""

    def test_send_message_returns_response(self):
        """Verifica se send_message retorna a resposta do LLM."""
        # Mocka toda a chain para evitar chamada à API
        with patch("app.services.chat_service.get_chat_prompt") as mock_prompt, \
             patch("app.services.chat_service.get_llm") as mock_llm:

            # Configura mock da resposta
            mock_response = MagicMock()
            mock_response.content = "Python é uma linguagem de programação."

            # Configura chain mockada
            mock_chain = MagicMock()
            mock_chain.invoke.return_value = mock_response

            # Configura o operador | para retornar a chain mockada
            mock_prompt.return_value.__or__ = MagicMock(return_value=mock_chain)

            # Importa após configurar os mocks
            from app.services.chat_service import ChatService

            chat = ChatService()
            response = chat.send_message("O que é Python?")

            assert response == "Python é uma linguagem de programação."

    def test_send_message_updates_history(self):
        """Verifica se o histórico é atualizado após enviar mensagem."""
        with patch("app.services.chat_service.get_chat_prompt") as mock_prompt, \
             patch("app.services.chat_service.get_llm") as mock_llm:

            mock_response = MagicMock()
            mock_response.content = "Resposta do assistente."

            mock_chain = MagicMock()
            mock_chain.invoke.return_value = mock_response
            mock_prompt.return_value.__or__ = MagicMock(return_value=mock_chain)

            from app.services.chat_service import ChatService

            chat = ChatService()
            chat.send_message("Pergunta teste")

            # Verifica se histórico contém a mensagem do usuário e do assistente
            assert len(chat.history) == 2
            assert isinstance(chat.history[0], HumanMessage)
            assert isinstance(chat.history[1], AIMessage)
            assert chat.history[0].content == "Pergunta teste"
            assert chat.history[1].content == "Resposta do assistente."

    def test_clear_history(self):
        """Verifica se clear_history limpa o histórico."""
        with patch("app.services.chat_service.get_chat_prompt") as mock_prompt, \
             patch("app.services.chat_service.get_llm") as mock_llm:

            mock_response = MagicMock()
            mock_response.content = "Resposta."

            mock_chain = MagicMock()
            mock_chain.invoke.return_value = mock_response
            mock_prompt.return_value.__or__ = MagicMock(return_value=mock_chain)

            from app.services.chat_service import ChatService

            chat = ChatService()
            chat.send_message("Mensagem 1")
            chat.send_message("Mensagem 2")

            assert len(chat.history) == 4  # 2 perguntas + 2 respostas

            chat.clear_history()

            assert len(chat.history) == 0

    def test_history_maintains_conversation_context(self):
        """Verifica se o histórico é passado para a chain nas chamadas."""
        with patch("app.services.chat_service.get_chat_prompt") as mock_prompt, \
             patch("app.services.chat_service.get_llm") as mock_llm:

            mock_response = MagicMock()
            mock_response.content = "Resposta."

            mock_chain = MagicMock()
            mock_chain.invoke.return_value = mock_response
            mock_prompt.return_value.__or__ = MagicMock(return_value=mock_chain)

            from app.services.chat_service import ChatService

            chat = ChatService()

            # Primeira mensagem
            chat.send_message("Primeira pergunta")

            # Segunda mensagem - histórico deve ser passado
            chat.send_message("Segunda pergunta")

            # Verifica que a chain foi chamada 2 vezes
            assert mock_chain.invoke.call_count == 2

            # Na segunda chamada, o histórico deve conter a primeira troca
            second_call = mock_chain.invoke.call_args_list[1]
            call_args = second_call[0][0]

            assert "history" in call_args
            # Histórico na 2ª chamada: 1ª pergunta + 1ª resposta = 2 mensagens
            # Mas o history é atualizado APÓS o invoke, então na 2ª chamada
            # o history ainda tem só 2 mensagens (da 1ª troca)
            assert len(call_args["history"]) >= 2


class TestPrompts:
    """Testes dos templates de prompt."""

    def test_exemplos_perguntas_respostas_exist(self):
        """Verifica se os exemplos de perguntas e respostas existem."""
        from app.llm.prompts import EXEMPLOS_PERGUNTAS_RESPOSTAS

        assert len(EXEMPLOS_PERGUNTAS_RESPOSTAS) > 0

        # Verifica estrutura dos exemplos
        for exemplo in EXEMPLOS_PERGUNTAS_RESPOSTAS:
            assert "pergunta" in exemplo
            assert "resposta" in exemplo
            assert len(exemplo["pergunta"]) > 0
            assert len(exemplo["resposta"]) > 0

    def test_system_prompt_defined(self):
        """Verifica se o system prompt está definido."""
        from app.llm.prompts import SYSTEM_PROMPT

        assert "Python" in SYSTEM_PROMPT
        assert "português" in SYSTEM_PROMPT.lower()

    def test_get_chat_prompt_returns_template(self):
        """Verifica se get_chat_prompt retorna um ChatPromptTemplate."""
        from app.llm.prompts import get_chat_prompt
        from langchain_core.prompts import ChatPromptTemplate

        prompt = get_chat_prompt()

        assert isinstance(prompt, ChatPromptTemplate)
