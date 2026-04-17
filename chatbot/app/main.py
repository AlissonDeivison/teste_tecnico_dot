"""
Ponto de entrada do chatbot via linha de comando.
Recebe perguntas do usuário e exibe respostas do assistente.
"""
from app.services.chat_service import ChatService


def main():
    """Loop principal do chatbot."""
    print("=" * 50)
    print("Chatbot Python - Assistente de Programação")
    print("Digite 'sair' para encerrar ou 'limpar' para reiniciar")
    print("=" * 50)

    chat = ChatService()

    while True:
        # Recebe pergunta do usuário via input de texto
        user_input = input("\nVocê: ").strip()

        # Comandos especiais
        if user_input.lower() == "sair":
            print("Até logo!")
            break

        if user_input.lower() == "limpar":
            chat.clear_history()
            print("Histórico limpo. Nova conversa iniciada.")
            continue

        if not user_input:
            print("Digite uma pergunta sobre Python.")
            continue

        # Envia para o LLM e exibe resposta
        try:
            response = chat.send_message(user_input)
            print(f"\nAssistente: {response}")
        except Exception as e:
            print(f"\nErro ao processar: {e}")


if __name__ == "__main__":
    main()
