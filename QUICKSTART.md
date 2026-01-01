# Quick Start Guide

## Installation

1. **Clone and navigate to the project:**
```bash
cd Agentic-RAG-with-LlamaIndex
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

## Running Examples

### 1. Router Engine

```python
from src.router_engine import get_router_query_engine

# Create router engine
query_engine = get_router_query_engine("data/papers/metagpt.pdf")

# Query - router automatically selects best method
response = query_engine.query("What is MetaGPT?")
print(response)
```

### 2. Tool Calling

```python
from src.document_tools import get_doc_tools

# Create tools
vector_tool, summary_tool = get_doc_tools("data/papers/metagpt.pdf", "metagpt")

# Use vector tool
result = vector_tool.fn("What is MetaGPT?", page_numbers=None)
print(result)
```

### 3. Agent Reasoning

```python
from src.agents import create_function_calling_agent
from src.document_tools import get_doc_tools

# Create tools
vector_tool, summary_tool = get_doc_tools("data/papers/metagpt.pdf", "metagpt")

# Create agent
agent = create_function_calling_agent([vector_tool, summary_tool])

# Query
response = agent.query("Tell me about agent roles in MetaGPT")
print(response)

# Conversational follow-up
response2 = agent.chat("How do they communicate?")
print(response2)
```

### 4. Multi-Document Agent

```python
from src.agents import create_multi_document_agent

# List of papers
papers = ["metagpt.pdf", "longlora.pdf", "selfrag.pdf"]

# Create agent
agent = create_multi_document_agent(papers, "data/papers/")

# Query across documents
response = agent.query("Compare evaluation datasets across these papers")
print(response)
```

## Running Notebooks

1. **Start Jupyter:**
```bash
jupyter notebook
```

2. **Navigate to notebooks directory and open:**
   - `01_router_engine.ipynb`
   - `02_tool_calling.ipynb`
   - `03_agent_reasoning.ipynb`
   - `04_multi_document_agent.ipynb`

## Project Structure

```
Agentic-RAG-with-LlamaIndex/
├── src/                    # Source code modules
│   ├── config.py          # Configuration
│   ├── router_engine.py   # Query routing
│   ├── document_tools.py  # Document tools
│   └── agents.py          # Agent implementations
├── notebooks/             # Jupyter notebooks
├── data/papers/          # PDF documents
├── docs/                 # Documentation
└── requirements.txt      # Dependencies
```

## Next Steps

- Read the [Architecture Overview](docs/architecture.md)
- Explore individual component docs:
  - [Router Engine](docs/router_engine.md)
  - [Tool Calling](docs/tool_calling.md)
  - [Agent Reasoning](docs/agent_reasoning.md)
  - [Multi-Document](docs/multi_document.md)

