"""
Cliente LangChain para integração com OpenAI.
Encapsula a configuração e instanciação do modelo de linguagem.
"""
# Classe do LangChain otimizada para chat, OpenAI é mais para completion
from langchain_openai import ChatOpenAI

from app.core.config import settings


def get_llm() -> ChatOpenAI:
    """
    Retorna instância configurada do modelo OpenAI.
    Usa ChatOpenAI pois é otimizado para conversação (chat completion).
    """
    return ChatOpenAI(
        api_key=settings.openai_api_key,
        model=settings.openai_model,
        temperature=0.7,  # Balanceia criatividade e consistência nas respostas
    )
