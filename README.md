# Agentic RAG System with LlamaIndex

A comprehensive implementation of an Agentic Retrieval-Augmented Generation (RAG) system built with LlamaIndex, featuring intelligent query routing, tool calling, agent reasoning loops, and multi-document support.

## 🎯 Project Overview

This project demonstrates a production-ready RAG system that combines multiple LlamaIndex capabilities to create intelligent document querying agents. The system intelligently routes queries, uses function calling for document retrieval, implements reasoning loops for complex queries, and extends to handle multiple documents simultaneously.

## ✨ Features

- **Intelligent Query Routing**: Automatically routes queries between summary-based and vector-based retrieval methods
- **Function Tool Calling**: Implements custom function tools for document querying with metadata filtering
- **Agent Reasoning Loop**: Builds autonomous agents that can reason through complex multi-step queries
- **Multi-Document Support**: Extends the system to handle and query across multiple documents simultaneously
- **Metadata Filtering**: Supports page-level filtering for precise document retrieval

## 📁 Project Structure

```
Agentic-RAG-with-LlamaIndex/
├── src/
│   ├── __init__.py
│   ├── config.py              # Configuration and API key management
│   ├── router_engine.py       # Query routing implementation
│   ├── document_tools.py      # Document querying tools
│   └── agents.py               # Agent implementations
├── notebooks/
│   ├── 01_router_engine.ipynb
│   ├── 02_tool_calling.ipynb
│   ├── 03_agent_reasoning.ipynb
│   └── 04_multi_document_agent.ipynb
├── data/
│   └── papers/                 # PDF documents
├── docs/
│   ├── architecture.md
│   ├── router_engine.md
│   ├── tool_calling.md
│   ├── agent_reasoning.md
│   └── multi_document.md
├── requirements.txt
├── .env.example
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- OpenAI API key

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd Agentic-RAG-with-LlamaIndex
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### Usage

#### 1. Router Engine

Intelligent query routing between summary and vector search:

```python
from src.router_engine import get_router_query_engine

query_engine = get_router_query_engine("data/papers/metagpt.pdf")
response = query_engine.query("What is MetaGPT?")
print(response)
```

#### 2. Tool Calling

Create custom function tools for document querying:

```python
from src.document_tools import get_doc_tools

vector_tool, summary_tool = get_doc_tools("data/papers/metagpt.pdf", "metagpt")
```

#### 3. Agent Reasoning Loop

Build an agent that can reason through complex queries:

```python
from src.agents import create_function_calling_agent

agent = create_function_calling_agent([vector_tool, summary_tool])
response = agent.query("Tell me about agent roles in MetaGPT and how they communicate")
```

#### 4. Multi-Document Agent

Query across multiple documents:

```python
from src.agents import create_multi_document_agent

papers = ["metagpt.pdf", "longlora.pdf", "selfrag.pdf"]
agent = create_multi_document_agent(papers, "data/papers/")
response = agent.query("Compare evaluation datasets across these papers")
```

## 📚 Documentation

- [Architecture Overview](docs/architecture.md)
- [Router Engine](docs/router_engine.md)
- [Tool Calling](docs/tool_calling.md)
- [Agent Reasoning](docs/agent_reasoning.md)
- [Multi-Document Support](docs/multi_document.md)

## 🔧 Configuration

The project uses environment variables for configuration. Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
```

## 📝 Notebooks

Interactive Jupyter notebooks are available in the `notebooks/` directory:

- `01_router_engine.ipynb` - Query routing implementation
- `02_tool_calling.ipynb` - Function tool creation
- `03_agent_reasoning.ipynb` - Agent reasoning loop
- `04_multi_document_agent.ipynb` - Multi-document agent

## 🧪 Examples

See the notebooks directory for complete examples of each component.

## 📄 License

MIT License

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
