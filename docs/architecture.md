# Architecture Overview

## System Architecture

The Agentic RAG System is built on LlamaIndex and implements a layered architecture that progressively adds capabilities:

```
┌─────────────────────────────────────────────────────────────┐
│                    User Query Interface                     │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              Multi-Document Agent Layer                      │
│  (Coordinates queries across multiple documents)            │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              Agent Reasoning Loop                            │
│  (Autonomous tool selection and multi-step reasoning)      │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              Router Engine / Tool Layer                     │
│  (Intelligent query routing and tool calling)               │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              Document Processing Layer                      │
│  (Vector Index | Summary Index)                             │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              Document Storage                               │
│  (PDF Documents)                                            │
└─────────────────────────────────────────────────────────────┘
```

## Components

### 1. Router Engine (`src/router_engine.py`)

The foundation layer that intelligently routes queries between two retrieval strategies:

- **Summary Index**: Tree-summarization approach for holistic document understanding
- **Vector Index**: Semantic search for specific context retrieval

**Key Features:**
- Automatic query routing based on query intent
- LLM-powered selector for optimal retrieval method
- Async processing for efficient summarization

### 2. Document Tools (`src/document_tools.py`)

Creates reusable function tools for document querying:

- **Vector Query Tool**: Function-based tool with metadata filtering support
- **Summary Query Tool**: Query engine tool for document summarization

**Key Features:**
- Page-level filtering for precise retrieval
- Configurable similarity search parameters
- Flexible tool naming for multi-document scenarios

### 3. Agent Reasoning (`src/agents.py`)

Implements autonomous agents with reasoning capabilities:

- **Function Calling Agent**: Uses tools autonomously to answer queries
- **Multi-Document Agent**: Extends capabilities to multiple documents

**Key Features:**
- Autonomous tool selection
- Multi-step reasoning
- Conversational context maintenance
- Multi-document synthesis

## Data Flow

1. **Document Ingestion**: PDFs are loaded and split into nodes
2. **Index Creation**: Nodes are indexed in both vector and summary indices
3. **Query Processing**: User queries are routed or processed by agents
4. **Tool Execution**: Appropriate tools are selected and executed
5. **Response Generation**: LLM synthesizes final response from retrieved context

## Design Principles

- **Modularity**: Each component is independently usable
- **Extensibility**: Easy to add new tools or documents
- **Intelligence**: Automatic routing and tool selection
- **Flexibility**: Supports both programmatic and conversational interfaces

