"""
Templates de prompts para o chatbot.
Define o comportamento e contexto do assistente de Python.
"""
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


# System prompt que define a persona e especialização do chatbot
SYSTEM_PROMPT = """Você é um assistente especializado em programação Python.
Seu objetivo é ajudar usuários com dúvidas sobre Python, fornecendo:
- Explicações claras e didáticas
- Exemplos de código quando apropriado
- Boas práticas de programação

Sempre responda em português brasileiro."""


# Exemplos de perguntas e respostas para demonstração do chatbot
EXEMPLOS_PERGUNTAS_RESPOSTAS = [
    {
        "pergunta": "Como criar uma lista em Python?",
        "resposta": """Em Python, você pode criar listas de várias formas:

1. Lista vazia:
```python
lista = []
```

2. Lista com valores iniciais:
```python
frutas = ["maçã", "banana", "laranja"]
numeros = [1, 2, 3, 4, 5]
```

3. Usando o construtor list():
```python
lista = list()
letras = list("abc")  # ['a', 'b', 'c']
```

4. List comprehension (forma pythonica):
```python
quadrados = [x**2 for x in range(5)]  # [0, 1, 4, 9, 16]
```"""
    },
    {
        "pergunta": "Como fazer um loop for em Python?",
        "resposta": """O loop for em Python itera sobre sequências:

1. Iterando sobre lista:
```python
frutas = ["maçã", "banana"]
for fruta in frutas:
    print(fruta)
```

2. Usando range():
```python
for i in range(5):
    print(i)  # 0, 1, 2, 3, 4
```

3. Com índice usando enumerate():
```python
for indice, valor in enumerate(frutas):
    print(f"{indice}: {valor}")
```"""
    },
    {
        "pergunta": "O que são f-strings?",
        "resposta": """F-strings (formatted string literals) são a forma moderna de formatar strings em Python (3.6+):

```python
nome = "Maria"
idade = 25

# F-string básica
print(f"Olá, {nome}!")

# Com expressões
print(f"Idade: {idade}, Ano que vem: {idade + 1}")

# Formatação de números
preco = 19.99
print(f"Preço: R${preco:.2f}")
```

Vantagens: mais legíveis e performáticas que .format() ou %."""
    },
]


def get_chat_prompt() -> ChatPromptTemplate:
    """
    Retorna template de prompt para conversação.
    MessagesPlaceholder permite manter histórico de mensagens.
    """
    return ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="history"),  # Histórico da conversa
        ("human", "{input}"),  # Pergunta atual do usuário
    ])
