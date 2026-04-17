# Chatbot Python - Assistente de Programação

Chatbot que utiliza LLM (GPT-4) para responder perguntas sobre programação Python.

## Desafio

Desenvolver um chatbot que:

1. Receba perguntas dos usuários via input de texto
2. Utilize LangChain para gerenciar o fluxo de conversação
3. Integre com modelo da OpenAI (GPT-4)
4. Responda perguntas sobre Python com explicações detalhadas

## Stack

- LangChain
- OpenAI GPT-4
- Pydantic Settings
- Pytest

## Arquitetura

Projeto estruturado em camadas:

```
app/
├── core/            # Configurações (API keys, settings)
├── llm/             # Integração com LangChain/OpenAI
│   ├── client.py    # Cliente ChatOpenAI
│   └── prompts.py   # Templates de prompt
├── services/        # Lógica do chatbot
└── main.py          # CLI (ponto de entrada)
```

### Camadas

**Core**: Configurações centralizadas, carrega variáveis do `.env`.

**LLM**: Encapsula integração com LangChain e OpenAI. Contém client e prompts.

**Services**: Orquestra a conversação, gerencia histórico de mensagens.

**Main**: Interface CLI para interação com o usuário.

### Benefícios

- Separação entre configuração, LLM e lógica de negócio
- Fácil troca de modelo (GPT-4 → GPT-3.5, Claude, etc)
- Prompts centralizados e reutilizáveis

## Instalação

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

## Configuração

```bash
# Copiar arquivo de exemplo
copy .env.example .env   # Windows
cp .env.example .env     # Linux/Mac

# Editar .env e adicionar sua API key
OPENAI_API_KEY=sk-sua-chave-aqui
OPENAI_MODEL=gpt-4  # opcional, padrão: gpt-4
```

## Executando o Chatbot

```bash
python -m app.main
```

### Comandos

| Comando | Descrição |
|---------|-----------|
| `sair` | Encerra o chatbot |
| `limpar` | Limpa histórico e inicia nova conversa |

### Exemplo de Uso

```
==================================================
Chatbot Python - Assistente de Programação
Digite 'sair' para encerrar ou 'limpar' para reiniciar
==================================================

Você: Como criar uma lista em Python?

Assistente: Em Python, você pode criar listas de várias formas:

1. Lista vazia:
lista = []

2. Lista com valores iniciais:
frutas = ["maçã", "banana", "laranja"]

3. List comprehension:
quadrados = [x**2 for x in range(5)]

Você: sair
Até logo!
```

## Testes

```bash
# Rodar todos os testes
pytest

# Rodar com output detalhado
pytest -v
```

### Estrutura de Testes

```
tests/
├── conftest.py           # Fixtures compartilhadas
└── test_chat_service.py  # Testes do serviço
```
