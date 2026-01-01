# Tool Calling

## Overview

Tool Calling enables the creation of reusable function tools for document querying. These tools can be used by agents to autonomously retrieve information from documents.

## Architecture

```
Document PDF
    │
    ▼
┌─────────────────────┐
│  Document Loader    │
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│  Node Parser        │  ← Splits into chunks
└─────────────────────┘
    │
    ├──────────────────┬──────────────────┐
    ▼                  ▼                  ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│   Vector    │  │   Summary   │  │  Metadata   │
│   Index     │  │   Index      │  │  Filters    │
└─────────────┘  └─────────────┘  └─────────────┘
    │                  │                  │
    ▼                  ▼                  ▼
┌─────────────────────────────────────────────┐
│         Function Tools                      │
│  - vector_query_tool                         │
│  - summary_tool                              │
└─────────────────────────────────────────────┘
```

## Tool Types

### 1. Vector Query Tool

A function-based tool that performs semantic similarity search.

**Features**:
- Configurable similarity search (top-k)
- Optional page-level filtering
- Returns precise context chunks

**Function Signature**:
```python
def vector_query(
    query: str,
    page_numbers: Optional[List[str]] = None
) -> str
```

**Example Usage**:
```python
from src.document_tools import get_doc_tools

vector_tool, summary_tool = get_doc_tools("data/papers/metagpt.pdf", "metagpt")

# Use directly
result = vector_tool.fn("What is MetaGPT?", page_numbers=["1", "2"])
```

### 2. Summary Query Tool

A query engine tool that provides holistic document summaries.

**Features**:
- Tree-summarization approach
- Async processing
- Holistic document understanding

**Best For**:
- Overview questions
- Summarization requests
- High-level understanding

## Metadata Filtering

The vector query tool supports page-level filtering:

```python
# Search across all pages
result = vector_tool.fn("What is MetaGPT?")

# Search specific pages only
result = vector_tool.fn("What is MetaGPT?", page_numbers=["1", "2", "3"])
```

## Usage

### Basic Usage

```python
from src.document_tools import get_doc_tools

# Create tools for a document
vector_tool, summary_tool = get_doc_tools(
    file_path="data/papers/metagpt.pdf",
    name="metagpt"
)
```

### With Agents

```python
from src.agents import create_function_calling_agent

# Create agent with tools
agent = create_function_calling_agent([vector_tool, summary_tool])

# Agent automatically selects and uses tools
response = agent.query("Tell me about MetaGPT")
```

## Configuration

- `chunk_size`: Document chunking size (default: 1024)
- `similarity_top_k`: Number of similar chunks to retrieve (default: 2)

## Advantages

1. **Reusability**: Tools can be used across different agents
2. **Flexibility**: Supports both function calls and query engines
3. **Metadata Support**: Page-level filtering for precise retrieval
4. **Agent Integration**: Seamlessly works with agent frameworks

## Use Cases

- Building custom RAG pipelines
- Creating document-specific tools
- Multi-document agent systems
- Precise context retrieval with filtering

