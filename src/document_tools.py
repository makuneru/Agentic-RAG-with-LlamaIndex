"""
Document Querying Tools

Creates function tools for vector-based and summary-based document querying
with support for metadata filtering.
"""

from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, SummaryIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.tools import FunctionTool, QueryEngineTool
from llama_index.core.vector_stores import MetadataFilters, FilterCondition
from typing import List, Optional


def get_doc_tools(
    file_path: str,
    name: str,
    chunk_size: int = 1024,
    similarity_top_k: int = 2
):
    """
    Create vector query and summary query tools from a document.
    
    Args:
        file_path (str): Path to the PDF file
        name (str): Name identifier for the document (used in tool names)
        chunk_size (int): Chunk size for document splitting (default: 1024)
        similarity_top_k (int): Number of top similar chunks to retrieve (default: 2)
        
    Returns:
        tuple: (vector_query_tool, summary_tool)
            - vector_query_tool: FunctionTool for vector-based queries
            - summary_tool: QueryEngineTool for summary-based queries
    """
    # Load and process documents
    documents = SimpleDirectoryReader(input_files=[file_path]).load_data()
    splitter = SentenceSplitter(chunk_size=chunk_size)
    nodes = splitter.get_nodes_from_documents(documents)
    vector_index = VectorStoreIndex(nodes)
    
    def vector_query(
        query: str, 
        page_numbers: Optional[List[str]] = None
    ) -> str:
        """
        Perform vector-based query over the document.
        
        Useful for specific questions that require precise context retrieval.
        Supports optional page-level filtering for targeted searches.
        
        Args:
            query (str): The query string to be embedded and searched
            page_numbers (Optional[List[str]]): Filter by specific page numbers.
                Leave as None for searching across all pages.
                Provide a list of page numbers (as strings) to filter results.
        
        Returns:
            str: Query response with relevant context
        """
        page_numbers = page_numbers or []
        metadata_dicts = [
            {"key": "page_label", "value": p} for p in page_numbers
        ]
        
        query_engine = vector_index.as_query_engine(
            similarity_top_k=similarity_top_k,
            filters=MetadataFilters.from_dicts(
                metadata_dicts,
                condition=FilterCondition.OR
            ) if metadata_dicts else None
        )
        response = query_engine.query(query)
        return str(response)
    
    # Create vector query tool
    vector_query_tool = FunctionTool.from_defaults(
        name=f"vector_tool_{name}",
        fn=vector_query
    )
    
    # Create summary index and query engine
    summary_index = SummaryIndex(nodes)
    summary_query_engine = summary_index.as_query_engine(
        response_mode="tree_summarize",
        use_async=True,
    )
    
    # Create summary tool
    summary_tool = QueryEngineTool.from_defaults(
        name=f"summary_tool_{name}",
        query_engine=summary_query_engine,
        description=(
            f"Useful for summarization questions related to {name}. "
            "Use ONLY when you want a holistic summary. "
            "Do NOT use for specific questions that require precise context."
        ),
    )

    return vector_query_tool, summary_tool

