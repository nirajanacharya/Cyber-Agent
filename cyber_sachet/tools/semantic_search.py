"""Semantic search tool implementation."""

import asyncio
from typing import List, Optional
from datetime import datetime
from ..models.search_result import SearchResult


async def semantic_search_tool(
    collection,
    query: str,
    n_results: int = 5,
    doc_type_filter: Optional[str] = None,
    min_relevance: float = 0.0
) -> List[SearchResult]:
    """
    Perform semantic search on cyber security documents.
    
    This is the primary search tool that uses vector embeddings to find
    semantically similar content across all indexed documents.
    
    Args:
        collection: ChromaDB collection
        query: The search query
        n_results: Number of results to return (default: 5, max: 20)
        doc_type_filter: Optional filter by "cyber_law" or "awareness"
        min_relevance: Minimum relevance score threshold (0.0-1.0)
    
    Returns:
        List of SearchResult objects sorted by relevance
    """
    n_results = min(max(1, n_results), 20)
    min_relevance = max(0.0, min(1.0, min_relevance))
    
    query_params = {
        "query_texts": [query],
        "n_results": n_results
    }
    
    if doc_type_filter:
        if doc_type_filter not in ["cyber_law", "awareness"]:
            raise ValueError(f"doc_type_filter must be 'cyber_law' or 'awareness', got {doc_type_filter}")
        query_params["where"] = {"doc_type": doc_type_filter}
    
    results = await asyncio.to_thread(collection.query, **query_params)
    
    search_results = []
    if results['documents'] and results['documents'][0]:
        for i in range(len(results['documents'][0])):
            distance = results['distances'][0][i] if 'distances' in results else 0
            relevance_score = max(0, 1 - distance)
            
            if relevance_score >= min_relevance:
                search_results.append(SearchResult(
                    content=results['documents'][0][i],
                    source=results['metadatas'][0][i]['source'],
                    doc_type=results['metadatas'][0][i]['doc_type'],
                    relevance_score=round(relevance_score, 3),
                    chunk_id=results['metadatas'][0][i]['chunk_id'],
                    metadata=results['metadatas'][0][i]
                ))
    
    return search_results
