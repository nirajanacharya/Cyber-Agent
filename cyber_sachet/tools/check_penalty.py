"""Penalty checking tool."""

from typing import Dict, Any
from .search_laws import search_laws_tool


async def check_penalty_tool(collection, crime_type: str) -> Dict[str, Any]:
    """
    Specialized tool to check penalties for specific cybercrimes.
    
    This tool first searches for penalty-related information in legal
    documents, then structures the results specifically for penalty queries.
    
    Args:
        collection: ChromaDB collection
        crime_type: Type of cybercrime (e.g., "hacking", "fraud", "data breach")
    
    Returns:
        Dictionary with:
            - crime_type: The crime type searched
            - found: Whether penalty information was found
            - details: List of relevant penalty text
            - sources: List of source documents
    """
    search_query = f"penalty punishment {crime_type} fine imprisonment sentence"
    results = await search_laws_tool(collection, search_query, n_results=3)
    
    penalty_info = {
        "crime_type": crime_type,
        "found": len(results) > 0,
        "details": [],
        "sources": []
    }
    
    for result in results:
        content_lower = result.content.lower()
        if any(word in content_lower for word in ['penalty', 'punishment', 'fine', 'imprisonment', 'sentence']):
            penalty_info["details"].append(result.content)
            if result.source not in penalty_info["sources"]:
                penalty_info["sources"].append(result.source)
    
    penalty_info["found"] = len(penalty_info["details"]) > 0
    
    return penalty_info
