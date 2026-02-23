"""Context building from search results."""

from typing import List, Set
from ..models.search_result import SearchResult


def build_context(search_results: List[SearchResult]) -> tuple[str, Set[str]]:
    """
    Build context string from search results.
    
    Args:
        search_results: List of SearchResult objects
    
    Returns:
        Tuple of (context_string, sources_used_set)
    """
    context_parts = []
    sources_used = set()
    
    for result in search_results:
        context_parts.append(
            f"[Source: {result.source}, Type: {result.doc_type}, Relevance: {result.relevance_score}]\n"
            f"{result.content}"
        )
        sources_used.add(result.source)
    
    context = "\n\n---\n\n".join(context_parts)
    
    return context, sources_used
