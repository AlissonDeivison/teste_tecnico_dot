"""
Serviço de chat que orquestra a comunicação com o LLM.
Gerencia o fluxo de conversação usando LangChain.
"""
from langchain_core.messages import HumanMessage, AIMessage

from app.llm.client import get_llm
from app.llm.prompts import get_chat_prompt


class ChatService:
    """
    Serviço que gerencia a conversação com o modelo de linguagem.
    Mantém histórico de mensagens para contexto da conversa.
    """

    def __init__(self):
        # Cria chain combinando prompt template + modelo
        self.chain = get_chat_prompt() | get_llm()
        # Histórico de mensagens para manter contexto
        self.history: list = []

    def send_message(self, user_input: str) -> str:
        """
        Envia mensagem do usuário e retorna resposta do assistente.
        Atualiza o histórico automaticamente.
        """
        # Invoca a chain com input do usuário e histórico
        response = self.chain.invoke({
            "input": user_input,
            "history": self.history,
        })

        # Atualiza histórico com a troca de mensagens
        self.history.append(HumanMessage(content=user_input))
        self.history.append(AIMessage(content=response.content))

        return response.content

    def clear_history(self) -> None:
        """Limpa o histórico de conversação."""
        self.history = []
