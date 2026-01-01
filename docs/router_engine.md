# Router Engine

## Overview

The Router Engine is the foundation of the Agentic RAG system. It intelligently routes queries between two complementary retrieval strategies to provide optimal answers.

## Architecture

```
Query Input
    │
    ▼
┌─────────────────────┐
│  LLM Selector       │  ← Determines query intent
└─────────────────────┘
    │
    ├──────────────────┬──────────────────┐
    ▼                  ▼                  ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│   Summary   │  │   Vector    │  │   Router    │
│   Index     │  │   Index     │  │   Decision  │
└─────────────┘  └─────────────┘  └─────────────┘
    │                  │
    ▼                  ▼
┌─────────────────────────────────┐
│      Query Engine Tools         │
└─────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────┐
│      Router Query Engine        │
└─────────────────────────────────┘
    │
    ▼
  Response
```

## Components

### Summary Index

**Purpose**: Provides holistic document understanding through tree-summarization.

**Best For**:
- "What is this document about?"
- "Give me an overview of..."
- "Summarize the main points..."

**Implementation**:
- Uses `tree_summarize` response mode
- Processes asynchronously for efficiency
- Builds hierarchical summaries

### Vector Index

**Purpose**: Retrieves specific context through semantic similarity search.

**Best For**:
- "What does the paper say about X?"
- "Find information on..."
- "What are the results for..."

**Implementation**:
- Embedding-based similarity search
- Returns top-k most relevant chunks
- Preserves document structure

### LLM Selector

**Purpose**: Automatically determines which retrieval method to use.

**How It Works**:
1. Analyzes query intent
2. Compares against tool descriptions
3. Selects optimal retrieval method
4. Routes query accordingly

## Usage

```python
from src.router_engine import get_router_query_engine

# Create router engine
query_engine = get_router_query_engine("data/papers/metagpt.pdf")

# Query - router automatically selects best method
response = query_engine.query("What is MetaGPT?")
print(response)
```

## Configuration Options

- `chunk_size`: Document chunking size (default: 1024)
- `llm`: Custom LLM instance (default: gpt-3.5-turbo)
- `embed_model`: Custom embedding model (default: text-embedding-ada-002)

## Advantages

1. **Automatic Optimization**: No need to manually choose retrieval method
2. **Best of Both Worlds**: Combines summarization and precise retrieval
3. **Intelligent Routing**: LLM understands query intent
4. **Transparent**: Verbose mode shows routing decisions

## Limitations

- Requires LLM call for routing (adds latency)
- May not always select optimal method
- Works best with clear query intent

