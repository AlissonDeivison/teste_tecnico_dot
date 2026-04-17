# Prova Técnica - Desenvolvedor Backend com Foco em IA

Este repositório contém as soluções para a prova técnica de desenvolvedor backend com foco em inteligência artificial.

## Estrutura do Repositório

Cada questão da prova está implementada em uma pasta separada:

| Questão | Descrição | Pasta |
|---------|-----------|-------|
| **Questão 1** | API REST para Biblioteca Virtual | `biblioteca_digital/` |
| **Questão 2** | Chatbot com IA Generativa (LangChain) | `chatbot/` |
| **Questão 3** | Busca Semântica com Embeddings e FAISS | `busca_semantica/` |

---

## Questão 1: API REST - Biblioteca Digital

**Tecnologias:** FastAPI, SQLAlchemy, SQLite, Pytest

**Funcionalidades:**
- Cadastro de livros (título, autor, data de publicação, resumo)
- Consulta de livros por título ou autor
- Documentação automática via Swagger

**Como executar:**
```bash
cd biblioteca_digital
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Testes:**
```bash
pytest -v
```

---

## Questão 2: Chatbot com IA Generativa

**Tecnologias:** LangChain, OpenAI, Python

**Funcionalidades:**
- Conversação via terminal com modelo GPT-4
- Gerenciamento de histórico de mensagens
- Templates de prompt otimizados para Python

**Como executar:**
```bash
cd chatbot
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
# Configure a OPENAI_API_KEY no arquivo .env
python -m app.main
```

**Testes:**
```bash
pytest -v
```

---

## Questão 3: Busca Semântica com Embeddings

**Tecnologias:** Sentence Transformers, FAISS, NumPy

**Funcionalidades:**
- Indexação de documentos de texto
- Geração de embeddings com modelo leve (all-MiniLM-L6-v2)
- Busca por similaridade semântica
- CLI interativo com menu de opções

**Como executar:**
```bash
cd busca_semantica
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Coloque arquivos .txt em data/documents/
python -m app.main
```

**Testes:**
```bash
pytest -v
```

---

## Requisitos Gerais

- Python 3.10+
- Ambiente virtual recomendado para cada projeto
- Variáveis de ambiente configuradas nos arquivos `.env` (exemplos em `.env.example`)

## Documentação Detalhada

Cada pasta contém seu próprio README.md com:
- Stack tecnológica
- Arquitetura do projeto
- Processo de implementação
- Exemplos de uso
