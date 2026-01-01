# Multi-Document Agent

## Overview

The Multi-Document Agent extends the agent reasoning capabilities to handle queries across multiple documents simultaneously. This enables comparison, synthesis, and cross-document analysis.

## Architecture

```
Multiple PDF Documents
    │
    ├──────────┬──────────┬──────────┐
    ▼          ▼          ▼          ▼
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│Paper 1 │ │Paper 2 │ │Paper 3 │ │  ...   │
└────────┘ └────────┘ └────────┘ └────────┘
    │          │          │          │
    ├──────────┴──────────┴──────────┤
    │                                  │
    ▼                                  ▼
┌─────────────────────────────────────────┐
│      Document Tools Creation            │
│  (Vector + Summary tools per document)  │
└─────────────────────────────────────────┘
    │
    ├──────────┬──────────┬──────────┐
    ▼          ▼          ▼          ▼
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│Tools 1 │ │Tools 2 │ │Tools 3 │ │  ...   │
└────────┘ └────────┘ └────────┘ └────────┘
    │          │          │          │
    └──────────┴──────────┴──────────┘
                │
                ▼
        ┌───────────────┐
        │  Multi-Doc    │
        │    Agent      │
        └───────────────┘
                │
                ▼
            Response
```

## Key Features

### Document Tool Creation

For each document, the system creates:
- **Vector Query Tool**: For specific context retrieval
- **Summary Query Tool**: For holistic summarization

Tools are named uniquely (e.g., `vector_tool_metagpt`, `summary_tool_longlora`)

### Unified Agent Interface

All document tools are available to a single agent:
- Agent can query any document
- Agent can compare across documents
- Agent can synthesize information

### Intelligent Tool Selection

The agent automatically:
- Selects relevant documents for queries
- Chooses appropriate tools (vector vs summary)
- Synthesizes information across documents

## Usage

### Creating Multi-Document Agent

```python
from src.agents import create_multi_document_agent

# List of papers
papers = [
    "metagpt.pdf",
    "longlora.pdf",
    "selfrag.pdf"
]

# Create agent
agent = create_multi_document_agent(
    paper_files=papers,
    data_dir="data/papers/"
)
```

### Querying Across Documents

```python
# Compare across documents
response = agent.query(
    "Compare the evaluation datasets used in LongLoRA and SelfRAG"
)

# Synthesize information
response = agent.query(
    "What are the common themes across these papers?"
)

# Specific document query
response = agent.query(
    "Tell me about MetaGPT's agent architecture"
)
```

### Complex Multi-Document Queries

```python
response = agent.query(
    "Tell me about the evaluation dataset used in LongLoRA, "
    "and then compare it with the evaluation approach in SelfRAG"
)
```

The agent will:
1. Use LongLoRA tools to find evaluation dataset info
2. Use SelfRAG tools to find evaluation approach
3. Compare and synthesize the information

## Tool Naming Convention

Tools are named based on document names:
- `vector_tool_{document_name}`
- `summary_tool_{document_name}`

Example:
- `vector_tool_metagpt`
- `summary_tool_longlora`
- `vector_tool_selfrag`

## Configuration

- `data_dir`: Directory containing PDF files (default: "data/papers/")
- `chunk_size`: Document chunking size (default: 1024)
- `similarity_top_k`: Similarity search results (default: 2)
- `llm`: Custom LLM instance
- `verbose`: Show reasoning process

## Advantages

1. **Cross-Document Analysis**: Compare and contrast information
2. **Synthesis**: Combine information from multiple sources
3. **Scalability**: Easy to add more documents
4. **Unified Interface**: Single agent for all documents

## Limitations

- Tool count increases with document count (2 tools per document)
- May require more tokens for complex queries
- Tool selection becomes more complex with many documents

## Use Cases

- Research paper comparison
- Multi-source information synthesis
- Literature review assistance
- Cross-document Q&A systems

## Example Workflow

```python
from src.agents import create_multi_document_agent

# Setup
papers = ["metagpt.pdf", "longlora.pdf", "selfrag.pdf"]
agent = create_multi_document_agent(papers, "data/papers/")

# Query 1: Single document focus
response1 = agent.query("What is MetaGPT?")

# Query 2: Cross-document comparison
response2 = agent.chat("How does LongLoRA compare to SelfRAG?")

# Query 3: Synthesis
response3 = agent.chat("What are common evaluation metrics across all papers?")
```

