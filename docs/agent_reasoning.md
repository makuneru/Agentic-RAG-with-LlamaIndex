# Agent Reasoning Loop

## Overview

The Agent Reasoning Loop implements autonomous agents that can reason through complex queries by autonomously selecting and using tools. This enables multi-step reasoning and conversational interactions.

## Architecture

```
User Query
    │
    ▼
┌─────────────────────┐
│  Agent Runner       │
│  (Orchestrates)     │
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│  Agent Worker       │
│  (Reasoning Logic)  │
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│  Tool Selection     │  ← Autonomous selection
└─────────────────────┘
    │
    ├──────────┬──────────┬──────────┐
    ▼          ▼          ▼          ▼
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│ Tool 1 │ │ Tool 2 │ │ Tool 3 │ │  ...   │
└────────┘ └────────┘ └────────┘ └────────┘
    │          │          │          │
    └──────────┴──────────┴──────────┘
                │
                ▼
        ┌───────────────┐
        │  LLM Response │  ← Synthesizes results
        └───────────────┘
                │
                ▼
            Response
```

## Key Components

### Agent Runner

Orchestrates the agent workflow:
- Manages conversation history
- Coordinates tool execution
- Handles response generation

### Agent Worker

Implements the reasoning logic:
- Analyzes queries
- Selects appropriate tools
- Executes tool calls
- Processes results

### Function Calling

The agent uses function calling to:
1. Understand available tools
2. Select relevant tools
3. Execute tool calls
4. Synthesize responses

## Reasoning Process

1. **Query Analysis**: Agent analyzes the user query
2. **Tool Selection**: Agent selects relevant tools from available set
3. **Tool Execution**: Selected tools are executed
4. **Result Processing**: Tool results are processed
5. **Response Synthesis**: LLM synthesizes final response
6. **Context Update**: Conversation context is updated

## Usage

### Basic Agent Creation

```python
from src.agents import create_function_calling_agent
from src.document_tools import get_doc_tools

# Create tools
vector_tool, summary_tool = get_doc_tools("data/papers/metagpt.pdf", "metagpt")

# Create agent
agent = create_function_calling_agent([vector_tool, summary_tool])

# Query
response = agent.query("Tell me about agent roles in MetaGPT")
```

### Conversational Agent

```python
# First query
response1 = agent.query("What is MetaGPT?")

# Follow-up query (uses context)
response2 = agent.chat("Tell me more about the evaluation datasets")

# Another follow-up
response3 = agent.chat("What were the results?")
```

### Multi-Step Reasoning

The agent can handle complex queries requiring multiple steps:

```python
response = agent.query(
    "Tell me about the agent roles in MetaGPT, "
    "and then explain how they communicate with each other."
)
```

The agent will:
1. Use vector tool to find information about agent roles
2. Use vector tool to find information about communication
3. Synthesize both pieces of information into a coherent response

## Features

### Autonomous Tool Selection

The agent automatically selects the best tool(s) for each query:
- Analyzes query intent
- Matches against tool descriptions
- Selects optimal tool(s)

### Multi-Step Reasoning

Can break down complex queries:
- Identifies sub-questions
- Executes multiple tool calls
- Synthesizes results

### Conversational Context

Maintains context across interactions:
- Remembers previous queries
- Uses context for follow-ups
- Provides coherent conversations

### Verbose Mode

Shows reasoning process:
- Tool selection decisions
- Tool execution results
- Response synthesis steps

## Configuration

- `temperature`: LLM temperature (default: 0 for deterministic)
- `verbose`: Show reasoning process (default: True)
- `llm`: Custom LLM instance

## Advantages

1. **Autonomy**: No manual tool selection needed
2. **Intelligence**: Understands complex queries
3. **Flexibility**: Handles various query types
4. **Conversational**: Maintains context

## Limitations

- Requires LLM calls for tool selection (adds latency)
- May make suboptimal tool selections
- Token usage increases with verbose mode

## Use Cases

- Complex document Q&A
- Multi-step information retrieval
- Conversational document interfaces
- Research assistance systems

