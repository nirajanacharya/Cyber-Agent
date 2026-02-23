"""Legal document search tool."""

from typing import List
from ..models.search_result import SearchResult
from .semantic_search import semantic_search_tool


async def search_laws_tool(collection, query: str, n_results: int = 3) -> List[SearchResult]:
    """
    Search only in cyber law documents.
    
    Specialized tool for searching Nepal's cyber law documents
    (IT Act 2063, Digital Security Act 2024).
    
    Args:
        collection: ChromaDB collection
        query: The search query
        n_results: Number of results to return (default: 3)
    
    Returns:
        List of SearchResult objects from legal documents only
    """
    return await semantic_search_tool(collection, query, n_results, "cyber_law")
