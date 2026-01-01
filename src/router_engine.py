"""
Router Engine Implementation

Intelligently routes queries between summary-based and vector-based retrieval methods.
"""

from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import SummaryIndex, VectorStoreIndex
from llama_index.core.tools import QueryEngineTool
from llama_index.core.query_engine.router_query_engine import RouterQueryEngine
from llama_index.core.selectors import LLMSingleSelector
from typing import Optional

from .config import get_openai_api_key


def get_router_query_engine(
    file_path: str,
    llm: Optional[OpenAI] = None,
    embed_model: Optional[OpenAIEmbedding] = None,
    chunk_size: int = 1024
):
    """
    Create a router query engine that intelligently routes queries.
    
    The router automatically selects between:
    - Summary-based retrieval: For holistic summarization questions
    - Vector-based retrieval: For specific context retrieval
    
    Args:
        file_path (str): Path to the PDF file
        llm (Optional[OpenAI]): LLM instance (defaults to gpt-3.5-turbo)
        embed_model (Optional[OpenAIEmbedding]): Embedding model (defaults to text-embedding-ada-002)
        chunk_size (int): Chunk size for document splitting (default: 1024)
        
    Returns:
        RouterQueryEngine: Configured router query engine
    """
    # Get API key
    _ = get_openai_api_key()
    
    # Initialize models if not provided
    llm = llm or OpenAI(model="gpt-3.5-turbo")
    embed_model = embed_model or OpenAIEmbedding(model="text-embedding-ada-002")
    
    # Load and process documents
    documents = SimpleDirectoryReader(input_files=[file_path]).load_data()
    splitter = SentenceSplitter(chunk_size=chunk_size)
    nodes = splitter.get_nodes_from_documents(documents)
    
    # Create indices
    summary_index = SummaryIndex(nodes)
    vector_index = VectorStoreIndex(nodes, embed_model=embed_model)
    
    # Create query engines
    summary_query_engine = summary_index.as_query_engine(
        response_mode="tree_summarize",
        use_async=True,
        llm=llm
    )
    vector_query_engine = vector_index.as_query_engine(llm=llm)
    
    # Create query engine tools
    summary_tool = QueryEngineTool.from_defaults(
        query_engine=summary_query_engine,
        description=(
            "Useful for summarization questions that require a holistic overview "
            "of the document content."
        ),
    )
    
    vector_tool = QueryEngineTool.from_defaults(
        query_engine=vector_query_engine,
        description=(
            "Useful for retrieving specific context, facts, or details "
            "from the document."
        ),
    )
    
    # Create router query engine
    query_engine = RouterQueryEngine(
        selector=LLMSingleSelector.from_defaults(),
        query_engine_tools=[
            summary_tool,
            vector_tool,
        ],
        verbose=True
    )
    
    return query_engine

