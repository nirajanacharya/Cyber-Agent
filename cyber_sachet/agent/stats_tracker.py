"""Agent statistics tracking."""

from typing import List, Dict, Any
from collections import Counter


def calculate_stats(query_history: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculate statistics from query history.
    
    Args:
        query_history: List of query result dictionaries
    
    Returns:
        Statistics dictionary
    """
    if not query_history:
        return {"total_queries": 0}
    
    all_tools = []
    for query in query_history:
        all_tools.extend(query['tools_used'])
    
    tool_counts = Counter(all_tools)
    
    avg_context_docs = sum(q['num_context_docs'] for q in query_history) / len(query_history)
    avg_duration = sum(q['query_duration_ms'] for q in query_history) / len(query_history)
    
    all_sources = set()
    for query in query_history:
        all_sources.update(query['sources_used'])
    
    return {
        "total_queries": len(query_history),
        "tool_usage": dict(tool_counts),
        "average_context_docs": round(avg_context_docs, 2),
        "average_duration_ms": round(avg_duration, 2),
        "unique_sources_used": len(all_sources),
        "sources": sorted(list(all_sources))
    }
