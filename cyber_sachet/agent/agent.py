"""
Cyber Sachet Agent - Async RAG Agent

This module provides the main Cyber Sachet Agent that uses Retrieval Augmented
Generation (RAG) to answer questions about cyber security and Nepal's cyber laws.
"""

from typing import List, Dict, Any
from datetime import datetime
from openai import AsyncOpenAI

from ..tools.base import CyberSachetTools
from .prompts import SYSTEM_PROMPT, get_user_message, detect_response_language
from .tool_selector import select_tools_for_query
from .query_executor import execute_tools
from .context_builder import build_context
from .response_generator import generate_response
from .stats_tracker import calculate_stats


class CyberSachetAgent:
    """
    Cyber Sachet Agent - AI Assistant for Cyber Security and Nepal Cyber Laws.
    
    This agent uses RAG (Retrieval Augmented Generation) with smart tool selection
    to provide accurate, well-cited answers about cyber security and Nepal's cyber laws.
    
    Features:
    - Smart tool selection based on query keywords
    - Always cites sources in responses
    - Tracks query history for evaluation
    - Async for better performance
    
    Attributes:
        tools: CyberSachetTools instance for document search
        client: AsyncOpenAI client for LLM calls
        query_history: List of all queries and responses
        system_prompt: System prompt for the agent
    """
    
    def __init__(self, tools: CyberSachetTools, async_client: AsyncOpenAI):
        """
        Initialize the agent.
        
        Args:
            tools: CyberSachetTools instance
            async_client: AsyncOpenAI client
        """
        self.tools = tools
        self.client = async_client
        self.query_history: List[Dict[str, Any]] = []
        self.system_prompt = SYSTEM_PROMPT
    
    async def query(
        self,
        user_question: str,
        n_context_docs: int = 5,
        verbose: bool = True,
        model: str = "gpt-4o-mini",
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """
        Query the agent with a question.
        
        This is the main method for interacting with the agent. It:
        1. Selects appropriate tools based on the question
        2. Retrieves relevant context documents
        3. Calls the LLM to generate a response
        4. Returns structured result with metadata
        
        Args:
            user_question: User's question
            n_context_docs: Number of context documents to retrieve (default: 5)
            verbose: Print progress information (default: True)
            model: OpenAI model to use (default: "gpt-4o-mini")
            temperature: Temperature for LLM (default: 0.7)
        
        Returns:
            Dictionary containing:
                - question: The user's question
                - answer: The agent's answer
                - sources_used: List of source documents used
                - tools_used: List of tools called
                - num_context_docs: Number of context documents retrieved
                - search_results: Detailed search results
                - timestamp: Query timestamp
                - model: Model used
        
        Example:
            >>> result = await agent.query(
            ...     "What are the penalties for hacking in Nepal?",
            ...     verbose=True
            ... )
            >>> print(result['answer'])
            >>> print(f"Sources: {result['sources_used']}")
        """
        query_start_time = datetime.now()
        
        if verbose:
            print(f"\nProcessing query: '{user_question}'")
        
        selected_tools = select_tools_for_query(user_question)
        
        if verbose:
            print(f"Selected tools: {', '.join(selected_tools)}")
        
        search_results, tools_used = await execute_tools(
            self.tools, selected_tools, user_question, n_context_docs, verbose
        )
        
        context, sources_used = build_context(search_results)

        response_language = detect_response_language(user_question)
        
        user_message = get_user_message(context, user_question)
        
        answer = await generate_response(
            self.client,
            self.system_prompt,
            user_message,
            response_language,
            model,
            temperature,
            verbose,
        )
        
        result = {
            "question": user_question,
            "answer": answer,
            "sources_used": sorted(list(sources_used)),
            "tools_used": tools_used,
            "num_context_docs": len(search_results),
            "search_results": [r.to_dict() for r in search_results],
            "timestamp": datetime.now().isoformat(),
            "model": model,
            "query_duration_ms": (datetime.now() - query_start_time).total_seconds() * 1000
        }
        
        self.query_history.append(result)
        
        return result
    
    async def quick_query(self, user_question: str, **kwargs) -> str:
        """
        Quick query that just returns the answer string.
        
        Args:
            user_question: User's question
            **kwargs: Additional arguments passed to query()
        
        Returns:
            The agent's answer as a string
        
        Example:
            >>> answer = await agent.quick_query("What is phishing?")
            >>> print(answer)
        """
        kwargs['verbose'] = kwargs.get('verbose', False)
        result = await self.query(user_question, **kwargs)
        return result["answer"]
    
    def get_query_history(self) -> List[Dict[str, Any]]:
        """
        Get history of all queries made to the agent.
        
        Returns:
            List of query result dictionaries
        """
        return self.query_history
    
    def clear_history(self):
        """Clear query history and tool call history."""
        self.query_history = []
        self.tools.clear_history()
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about agent usage.
        
        Returns:
            Dictionary with usage statistics
        """
        return calculate_stats(self.query_history)


def create_agent(tools: CyberSachetTools, async_client: AsyncOpenAI) -> CyberSachetAgent:
    """
    Factory function to create a CyberSachetAgent instance.
    
    Args:
        tools: CyberSachetTools instance
        async_client: AsyncOpenAI client
    
    Returns:
        Configured CyberSachetAgent instance
    """
    return CyberSachetAgent(tools, async_client)
