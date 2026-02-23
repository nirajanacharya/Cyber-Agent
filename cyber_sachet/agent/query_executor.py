"""Tool execution logic."""

from typing import List
from ..tools.base import CyberSachetTools
from ..models.search_result import SearchResult
from .tool_selector import extract_crime_type


async def execute_tools(
    tools: CyberSachetTools,
    selected_tools: List[str],
    user_question: str,
    n_context_docs: int = 5,
    verbose: bool = True
) -> tuple[List[SearchResult], List[str]]:
    """
    Execute selected tools and collect search results.
    
    Args:
        tools: CyberSachetTools instance
        selected_tools: List of tool names to execute
        user_question: User's question
        n_context_docs: Number of documents to retrieve
        verbose: Print progress information
    
    Returns:
        Tuple of (search_results, tools_used)
    """
    search_results: List[SearchResult] = []
    tools_used = []
    
    for tool_name in selected_tools:
        if tool_name == 'check_penalty_tool':
            crime_type = extract_crime_type(user_question)
            if verbose:
                print(f"Checking penalties for: {crime_type}")
            penalty_info = await tools.check_penalty_tool(crime_type)
            tools_used.append('check_penalty_tool')
        
        elif tool_name == 'search_laws_tool':
            if verbose:
                print("Searching legal documents...")
            results = await tools.search_laws_tool(user_question, n_results=n_context_docs)
            search_results.extend(results)
            tools_used.append('search_laws_tool')
        
        elif tool_name == 'search_awareness_tool':
            if verbose:
                print("Searching awareness guides...")
            results = await tools.search_awareness_tool(user_question, n_results=n_context_docs)
            search_results.extend(results)
            tools_used.append('search_awareness_tool')
        
        elif tool_name == 'semantic_search_tool':
            if verbose:
                print("Performing semantic search...")
            results = await tools.semantic_search_tool(user_question, n_results=n_context_docs)
            search_results.extend(results)
            tools_used.append('semantic_search_tool')
    

    tools_used = list(dict.fromkeys(tools_used))
    
    if verbose and search_results:
        print(f"Retrieved {len(search_results)} relevant documents")
        for i, r in enumerate(search_results[:3], 1):
            print(f"  {i}. {r.source} (relevance: {r.relevance_score})")
    
    return search_results, tools_used
