"""Base tools class that combines all tool functionality."""

from typing import List, Dict, Any, Optional
from datetime import datetime

from .tool_logger import ToolLogger
from .semantic_search import semantic_search_tool
from .search_laws import search_laws_tool
from .search_awareness import search_awareness_tool
from .document_sources import get_document_sources_tool
from .check_penalty import check_penalty_tool
from ..models.search_result import SearchResult


class CyberSachetTools:
    """
    Async Tool Collection for Cyber Sachet Agent.
    
    Provides async tools for searching through cyber security documents
    and Nepal's cyber law documentation. All tools are observable with
    call logging for testing and evaluation.
    
    Attributes:
        collection: ChromaDB collection for vector search
        embedding_function: OpenAI embedding function
        logger: ToolLogger instance for tracking calls
    """
    
    def __init__(self, collection, embedding_function, enable_logging: bool = True):
        """
        Initialize tools.
        
        Args:
            collection: ChromaDB collection
            embedding_function: Embedding function for queries
            enable_logging: Enable tool call logging
        """
        self.collection = collection
        self.embedding_function = embedding_function
        self.logger = ToolLogger(enable_logging)
    
    def get_tool_call_history(self):
        """Get history of all tool calls."""
        return self.logger.get_history()
    
    def clear_history(self):
        """Clear tool call history."""
        self.logger.clear_history()
    
    def get_tool_stats(self) -> Dict[str, Any]:
        """Get statistics about tool usage."""
        return self.logger.get_stats()
    
    async def semantic_search_tool(
        self,
        query: str,
        n_results: int = 5,
        doc_type_filter: Optional[str] = None,
        min_relevance: float = 0.0
    ) -> List[SearchResult]:
        """
        Perform semantic search on cyber security documents.
        
        Args:
            query: The search query
            n_results: Number of results to return (default: 5, max: 20)
            doc_type_filter: Optional filter by "cyber_law" or "awareness"
            min_relevance: Minimum relevance score threshold (0.0-1.0)
        
        Returns:
            List of SearchResult objects sorted by relevance
        """
        start_time = datetime.now()
        
        results = await semantic_search_tool(
            self.collection, query, n_results, doc_type_filter, min_relevance
        )
        
        duration = (datetime.now() - start_time).total_seconds() * 1000
        self.logger.log_call("semantic_search_tool", {
            "query": query, "n_results": n_results,
            "doc_type_filter": doc_type_filter, "min_relevance": min_relevance
        }, results, duration)
        
        return results
    
    async def search_laws_tool(self, query: str, n_results: int = 3) -> List[SearchResult]:
        """Search only in cyber law documents."""
        start_time = datetime.now()
        
        results = await search_laws_tool(self.collection, query, n_results)
        
        duration = (datetime.now() - start_time).total_seconds() * 1000
        self.logger.log_call("search_laws_tool", {"query": query, "n_results": n_results}, results, duration)
        
        return results
    
    async def search_awareness_tool(self, query: str, n_results: int = 3) -> List[SearchResult]:
        """Search only in cyber awareness documents."""
        start_time = datetime.now()
        
        results = await search_awareness_tool(self.collection, query, n_results)
        
        duration = (datetime.now() - start_time).total_seconds() * 1000
        self.logger.log_call("search_awareness_tool", {"query": query, "n_results": n_results}, results, duration)
        
        return results
    
    async def get_document_sources_tool(self) -> Dict[str, Any]:
        """Get list of all indexed document sources with statistics."""
        start_time = datetime.now()
        
        result = await get_document_sources_tool(self.collection)
        
        duration = (datetime.now() - start_time).total_seconds() * 1000
        self.logger.log_call("get_document_sources_tool", {}, result, duration)
        
        return result
    
    async def check_penalty_tool(self, crime_type: str) -> Dict[str, Any]:
        """Specialized tool to check penalties for specific cybercrimes."""
        start_time = datetime.now()
        
        result = await check_penalty_tool(self.collection, crime_type)
        
        duration = (datetime.now() - start_time).total_seconds() * 1000
        self.logger.log_call("check_penalty_tool", {"crime_type": crime_type}, result, duration)
        
        return result


def create_tools(collection, embedding_function, enable_logging: bool = True) -> CyberSachetTools:
    """
    Factory function to create a CyberSachetTools instance.
    
    Args:
        collection: ChromaDB collection
        embedding_function: Embedding function for queries
        enable_logging: Enable tool call logging
    
    Returns:
        Configured CyberSachetTools instance
    """
    return CyberSachetTools(collection, embedding_function, enable_logging)
