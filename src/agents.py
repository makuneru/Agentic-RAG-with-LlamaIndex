"""
Agent Implementations

Creates function calling agents with reasoning capabilities for document querying.
"""

from llama_index.llms.openai import OpenAI
from llama_index.core.agent import AgentRunner
from llama_index.agent.openai import OpenAIAgentWorker
from llama_index.core.tools import FunctionTool, QueryEngineTool
from typing import List, Optional

from .config import get_openai_api_key
from .document_tools import get_doc_tools


def create_function_calling_agent(
    tools: List,
    llm: Optional[OpenAI] = None,
    temperature: float = 0,
    verbose: bool = True
) -> AgentRunner:
    """
    Create a function calling agent with reasoning capabilities.
    
    The agent can autonomously select and use tools to answer complex queries,
    including multi-step reasoning tasks.
    
    Args:
        tools (List): List of tools (FunctionTool or QueryEngineTool instances)
        llm (Optional[OpenAI]): LLM instance (defaults to gpt-3.5-turbo)
        temperature (float): LLM temperature (default: 0 for deterministic responses)
        verbose (bool): Whether to print verbose output (default: True)
        
    Returns:
        AgentRunner: Configured agent instance
    """
    # Get API key
    _ = get_openai_api_key()
    
    # Initialize LLM if not provided
    llm = llm or OpenAI(model="gpt-3.5-turbo", temperature=temperature)
    
    # Create agent worker (updated for LlamaIndex 0.11+)
    agent_worker = OpenAIAgentWorker.from_tools(
        tools, 
        llm=llm, 
        verbose=verbose
    )
    
    # Create agent runner
    agent = AgentRunner(agent_worker)
    
    return agent


def create_multi_document_agent(
    paper_files: List[str],
    data_dir: str = "data/papers/",
    llm: Optional[OpenAI] = None,
    verbose: bool = True
) -> AgentRunner:
    """
    Create an agent that can query across multiple documents.
    
    The agent has access to vector and summary tools for each document,
    allowing it to compare, contrast, and synthesize information across papers.
    
    Args:
        paper_files (List[str]): List of PDF filenames
        data_dir (str): Directory containing the PDF files (default: "data/papers/")
        llm (Optional[OpenAI]): LLM instance (defaults to gpt-3.5-turbo)
        verbose (bool): Whether to print verbose output (default: True)
        
    Returns:
        AgentRunner: Configured multi-document agent instance
    """
    # Collect tools for all documents
    all_tools = []
    paper_to_tools_dict = {}
    
    for paper in paper_files:
        file_path = f"{data_dir}{paper}" if not paper.startswith(data_dir) else paper
        name = paper.replace(".pdf", "").replace(data_dir, "")
        
        print(f"Loading tools for paper: {paper}")
        vector_tool, summary_tool = get_doc_tools(file_path, name)
        paper_to_tools_dict[paper] = [vector_tool, summary_tool]
        all_tools.extend([vector_tool, summary_tool])
    
    print(f"Created agent with {len(all_tools)} tools across {len(paper_files)} documents")
    
    # Create agent with all tools
    agent = create_function_calling_agent(
        all_tools,
        llm=llm,
        verbose=verbose
    )
    
    return agent

