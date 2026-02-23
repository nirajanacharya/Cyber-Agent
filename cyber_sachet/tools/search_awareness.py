"""Cyber awareness search tool."""

from typing import List
from ..models.search_result import SearchResult
from .semantic_search import semantic_search_tool


async def search_awareness_tool(collection, query: str, n_results: int = 3) -> List[SearchResult]:
    """
    Search only in cyber awareness documents.
    
    Specialized tool for searching cyber security awareness guides
    and best practices.
    
    Args:
        collection: ChromaDB collection
        query: The search query
        n_results: Number of results to return (default: 3)
    
    Returns:
        List of SearchResult objects from awareness documents only
    """
    return await semantic_search_tool(collection, query, n_results, "awareness")
