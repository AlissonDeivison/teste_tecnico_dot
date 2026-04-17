# Busca Semântica com Embeddings e FAISS

Sistema de busca semântica que utiliza embeddings para encontrar documentos relevantes por similaridade de significado.

## Desafio

Desenvolver um sistema que:

1. Utilize um conjunto de documentos de texto
2. Gere embeddings usando um modelo de embeddings
3. Armazene os embeddings em uma vector store (FAISS)
4. Implemente busca semântica por similaridade

## Stack

- Sentence Transformers (Hugging Face)
- FAISS (Facebook AI Similarity Search)
- Pydantic Settings
- Pytest

## Arquitetura

```
app/
├── core/            # Configurações
├── embeddings/      # Geração de embeddings
├── vectorstore/     # Armazenamento FAISS
├── services/        # Lógica de busca
└── main.py          # CLI
data/
├── documents/       # Documentos de texto para indexar
└── faiss_index.*    # Índice FAISS persistido
```

---

## Processo de Criação de Embeddings

### 1. O que são Embeddings?

Embeddings são representações vetoriais de texto em um espaço de alta dimensão. Textos com significados semelhantes ficam próximos nesse espaço, permitindo busca por similaridade.

```
"Como criar uma lista em Python?" → [0.12, -0.45, 0.78, ..., 0.33]  (384 dimensões)
```

### 2. Modelo Utilizado

Utilizei o modelo **sentence-transformers/all-MiniLM-L6-v2**:

| Característica | Valor |
|----------------|-------|
| Parâmetros | 22M |
| Dimensões | 384 |
| Idiomas | 100+ |
| Tamanho | ~23MB |

**Por que este modelo?**
- Leve e eficiente (22M vs 300M parâmetros)
- Download automático sem autenticação necessária
- Excelente custo-benefício para projetos de busca semântica
- Suporte multilíngue adequado para português

### 3. API do Sentence Transformers

O modelo usa a API padrão do sentence-transformers:

```python
# Para documentos (indexação)
embeddings = model.encode(["Documento 1", "Documento 2"])

# Para queries (busca)
query_embedding = model.encode("Minha pergunta")
```

**Como funciona:**
- Método único `encode()` para queries e documentos
- Vetores normalizados automaticamente
- Similaridade por cosseno no espaço vetorial

### 4. Fluxo de Criação

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────┐
│  Documento  │ ──▶ │    encode()      │ ──▶ │  Embedding  │
│   (texto)   │     │   (modelo HF)    │     │  (vetor)    │
└─────────────┘     └──────────────────┘     └─────────────┘
      │                                             │
      │         "Python é uma linguagem..."         │
      │                     ↓                       │
      │         [0.12, -0.45, 0.78, ..., 0.33]     │
      │                                             │
      └─────────────────────────────────────────────┘
```

---

## Armazenamento na Vector Store (FAISS)

### 1. O que é FAISS?

FAISS (Facebook AI Similarity Search) é uma biblioteca para busca eficiente de vetores similares. Desenvolvida pelo Facebook AI Research, é otimizada para:

- Busca em milhões de vetores
- Baixa latência
- Operações em memória ou disco

### 2. Tipo de Índice

Utilizamos **IndexFlatIP** (Inner Product):

```python
index = faiss.IndexFlatIP(384)  # 384 = dimensão do embedding
```

| Índice | Descrição | Uso |
|--------|-----------|-----|
| IndexFlatL2 | Distância Euclidiana | Quando magnitude importa |
| **IndexFlatIP** | Produto Interno | Similaridade cosseno (normalizado) |
| IndexIVF | Índice invertido | Datasets grandes (milhões) |

**Por que IndexFlatIP?**
- Equivale à similaridade cosseno quando vetores são normalizados
- Busca exata (sem aproximação)
- Simples e eficiente para datasets pequenos/médios

### 3. Normalização

Antes de adicionar ao índice, normalizamos os vetores:

```python
faiss.normalize_L2(embeddings)
```

Isso garante que o produto interno seja equivalente à similaridade cosseno:

```
cos(A, B) = (A · B) / (||A|| × ||B||)

Se ||A|| = ||B|| = 1 (normalizados):
cos(A, B) = A · B  (produto interno)
```

### 4. Estrutura de Armazenamento

```
data/
├── faiss_index.faiss   # Índice binário FAISS
└── faiss_index.docs    # Mapeamento índice → documento
```

O FAISS armazena apenas vetores. Mantemos um arquivo separado com os textos originais para retornar nas buscas.

### 5. Fluxo de Indexação

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Documentos  │ ──▶ │ Embeddings  │ ──▶ │    FAISS    │
│   (lista)   │     │  (matriz)   │     │   (índice)  │
└─────────────┘     └─────────────┘     └─────────────┘
      │                   │                    │
      │                   ▼                    │
      │            normalize_L2()              │
      │                   │                    │
      │                   ▼                    │
      │             index.add()                │
      │                   │                    │
      └───────────────────┼────────────────────┘
                          ▼
                   ┌─────────────┐
                   │    Disco    │
                   │  .faiss     │
                   │  .docs      │
                   └─────────────┘
```

### 6. Fluxo de Busca

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│    Query    │ ──▶ │  Embedding  │ ──▶ │   search()  │
│   (texto)   │     │   (vetor)   │     │   (FAISS)   │
└─────────────┘     └─────────────┘     └─────────────┘
                                               │
                                               ▼
                                        ┌─────────────┐
                                        │  Top-K IDs  │
                                        │  + Scores   │
                                        └─────────────┘
                                               │
                                               ▼
                                        ┌─────────────┐
                                        │ Documentos  │
                                        │ Relevantes  │
                                        └─────────────┘
```

---

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

## Executando

```bash
# Iniciar o sistema interativo
python -m app.main
```

O sistema inicia um menu interativo:
1. **Na inicialização**: verifica se o índice existe, se não, indexa automaticamente
2. **Menu**: opções para buscar, reindexar ou ver demonstração
3. **Busca**: digite sua query e veja os resultados por similaridade

## Testes

```bash
pytest -v
```
