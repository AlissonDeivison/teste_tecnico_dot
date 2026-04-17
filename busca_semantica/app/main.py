"""
Sistema interativo de busca semântica.
Loop principal que indexa documentos e permite buscas por similaridade.
"""
from app.services.search_service import SearchService


def print_menu():
    """Exibe o menu de opções."""
    print("\n" + "=" * 50)
    print("BUSCA SEMÂNTICA - Menu")
    print("=" * 50)
    print("1. Buscar documentos")
    print("2. Reindexar documentos")
    print("3. Demonstração")
    print("0. Sair")
    print("=" * 50)


def ensure_index(service: SearchService) -> bool:
    """
    Garante que o índice existe.
    Se não existir, tenta indexar documentos automaticamente.

    Returns:
        True se índice está pronto, False se falhou
    """
    if service.index_exists():
        print("✓ Índice encontrado. Carregando...")
        service.load_index()
        print(f"  {len(service)} documentos disponíveis para busca.")
        return True

    print("⚠ Índice não encontrado. Indexando documentos...")
    try:
        count = service.index_from_directory()
        service.save_index()
        print(f"✓ {count} documentos indexados com sucesso!")
        return True
    except FileNotFoundError as e:
        print(f"✗ Erro: {e}")
        print("  Crie a pasta data/documents/ e adicione arquivos .txt")
        return False
    except ValueError as e:
        print(f"✗ Erro: {e}")
        return False


def cmd_search(service: SearchService):
    """Loop de busca interativa."""
    query = input("\nDigite sua busca (ou 'voltar' para menu): ").strip()

    if query.lower() == 'voltar' or not query:
        return

    print(f"\nBuscando: '{query}'\n")
    results = service.search(query)

    if not results:
        print("Nenhum resultado encontrado.")
        return

    print(f"Top {len(results)} resultados:\n")
    for i, result in enumerate(results, 1):
        score = result["score"]
        doc = result["document"]
        preview = doc[:200] + "..." if len(doc) > 200 else doc
        print(f"{i}. [Score: {score:.4f}]")
        print(f"   {preview}\n")


def cmd_demo():
    """Demonstração com documentos e buscas de exemplo (índice separado em memória)."""
    print("=" * 50)
    print("DEMONSTRAÇÃO - Busca Semântica")
    print("=" * 50)

    # Cria serviço fresh apenas para demo (não persiste em disco)
    demo_service = SearchService()

    # Documentos de exemplo sobre Python
    documents = [
        "Listas em Python são estruturas de dados mutáveis que armazenam coleções ordenadas de elementos. Você pode criar uma lista usando colchetes: minha_lista = [1, 2, 3]. Listas suportam operações como append(), remove() e sort().",

        "Dicionários em Python são estruturas de dados que armazenam pares chave-valor. São criados usando chaves: meu_dict = {'nome': 'João', 'idade': 25}. Dicionários são muito eficientes para busca por chave.",

        "Funções em Python são definidas usando a palavra-chave def. Elas permitem reutilizar código e organizar a lógica do programa. Funções podem receber parâmetros e retornar valores usando return.",

        "Classes em Python são usadas para programação orientada a objetos. Uma classe define atributos e métodos que descrevem o comportamento de objetos. Use a palavra-chave class para criar uma classe.",

        "List comprehension é uma forma concisa de criar listas em Python. A sintaxe é [expressão for item in iterável]. Por exemplo: quadrados = [x**2 for x in range(10)] cria uma lista com quadrados de 0 a 9.",

        "O tratamento de exceções em Python é feito com try/except. Isso permite capturar erros durante a execução e tratá-los adequadamente, evitando que o programa pare inesperadamente.",

        "Decorators em Python são funções que modificam o comportamento de outras funções. São aplicados usando @nome_decorator acima da definição da função. São muito usados em frameworks web.",

        "Geradores em Python são funções que usam yield ao invés de return. Eles permitem iterar sobre grandes conjuntos de dados de forma eficiente, sem carregar tudo na memória de uma vez.",
    ]

    print("\n1. Indexando documentos de exemplo...")
    count = demo_service.index_documents(documents)
    print(f"   ✓ {count} documentos indexados\n")

    # Queries de exemplo
    queries = [
        "Como criar uma lista em Python?",
        "O que são dicionários?",
        "Como tratar erros no código?",
    ]

    print("2. Executando buscas de exemplo:\n")

    for query in queries:
        print("-" * 40)
        print(f"Query: '{query}'\n")

        results = demo_service.search(query, top_k=2)

        for i, result in enumerate(results, 1):
            score = result["score"]
            doc = result["document"][:150] + "..."
            print(f"   {i}. [Score: {score:.4f}]")
            print(f"      {doc}\n")

    print("=" * 50)
    print("Demonstração concluída!")
    print("  (Índice de demo descartado - não afeta documentos reais)")


def cmd_reindex(service: SearchService):
    """Reindexa documentos do diretório."""
    print("\nReindexando documentos...")
    try:
        # Cria novo serviço para limpar índice anterior
        service.store.index.reset()
        service.store.documents.clear()

        count = service.index_from_directory()
        service.save_index()
        print(f"✓ {count} documentos reindexados com sucesso!")
    except FileNotFoundError as e:
        print(f"✗ Erro: {e}")
        print("  Crie a pasta data/documents/ e adicione arquivos .txt")
    except ValueError as e:
        print(f"✗ Erro: {e}")


def main():
    """Loop principal do sistema."""
    print("\n" + "=" * 50)
    print("BEM-VINDO AO SISTEMA DE BUSCA SEMÂNTICA")
    print("=" * 50)

    service = SearchService()

    # 1. Verifica/cria índice na inicialização
    index_ready = ensure_index(service)

    if not index_ready:
        print("\n⚠ Sistema iniciado sem índice.")
        print("  Use opção 2 para indexar após adicionar documentos.")

    # 2. Loop do menu interativo
    while True:
        print_menu()
        choice = input("Escolha uma opção: ").strip()

        if choice == "1":
            if len(service) == 0:
                print("\n✗ Índice vazio. Adicione documentos e use opção 2.")
            else:
                cmd_search(service)

        elif choice == "2":
            cmd_reindex(service)

        elif choice == "3":
            cmd_demo()

        elif choice == "0":
            print("\nAté logo!")
            break

        else:
            print("\n✗ Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
