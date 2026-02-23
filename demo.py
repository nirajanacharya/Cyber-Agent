"""
Cyber Sachet Agent - Demo Script
Demonstrates the RAG-based agent for cyber security and Nepal cyber law queries
"""

import asyncio
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
import chromadb
from chromadb.utils import embedding_functions

from cyber_sachet.tools.base import create_tools
from cyber_sachet.agent.agent import create_agent
from cyber_sachet.database.document_loader import load_documents


async def main():
    """Initialize and run demo queries through the agent."""
    
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    if not openai_api_key:
        print("ERROR: OPENAI_API_KEY not found in .env file")
        return
    
    print("Initializing Cyber Sachet Agent...")
    print("-" * 70)
    
    client = AsyncOpenAI(api_key=openai_api_key)
    print("OpenAI client initialized")
    
    db_client = chromadb.Client()
    print("ChromaDB client initialized")
    
    embedding_fn = embedding_functions.OpenAIEmbeddingFunction(
        api_key=openai_api_key,
        model_name="text-embedding-3-small"
    )
    print("Embedding function configured")
    
    doc_collection = db_client.get_or_create_collection(
        name="cyber_sachet",
        embedding_function=embedding_fn
    )
    print(f"Document collection ready ({doc_collection.count()} documents)")
    
    if doc_collection.count() == 0:
        print("\nLoading documents from docs/ directory...")
        load_stats = load_documents(doc_collection, docs_folder="docs/", chunk_size=500)
        print(f"Loaded {load_stats['total_chunks']} chunks from {len(load_stats['files_loaded'])} files")
        print(f"Document types: {load_stats['doc_types']}")
    
    agent_tools = create_tools(doc_collection, embedding_fn, enable_logging=True)
    print("Tools initialized")
    
    cyber_agent = create_agent(agent_tools, client)
    print("Agent initialized")
    
    print("\n" + "-" * 70)
    print("AGENT READY - Running demo queries")
    print("-" * 70)
    
    test_queries = [
        "What is phishing?",
        "What are the penalties for hacking in Nepal?",
        "How can I create a strong password?"
    ]
    
    for idx, query in enumerate(test_queries, 1):
        print(f"\n\nQuery {idx}: {query}")
        print("-" * 70)
        
        query_result = await cyber_agent.query(query, verbose=True, n_context_docs=3)
        
        print("\nResponse:")
        print("-" * 70)
        print(query_result['answer'])
        print("\n" + "-" * 70)
        print(f"Sources: {', '.join(query_result['sources_used'])}")
        print(f"Tools used: {', '.join(query_result['tools_used'])}")
        print(f"Processing time: {query_result['query_duration_ms']:.2f}ms")
        print("-" * 70)
    
    print("\n\n" + "-" * 70)
    print("AGENT STATISTICS")
    print("-" * 70)
    agent_stats = cyber_agent.get_stats()
    print(f"Total queries processed: {agent_stats['total_queries']}")
    print(f"Tool usage breakdown: {agent_stats['tool_usage']}")
    print(f"Average documents per query: {agent_stats['average_context_docs']}")
    print(f"Average processing time: {agent_stats['average_duration_ms']:.2f}ms")
    print(f"Unique sources referenced: {agent_stats['unique_sources_used']}")
    print("-" * 70)
    
    print("\nDemo completed successfully")
    print("\nFor interactive usage, see:")
    print("  - cybersachet_modular.ipynb")
    print("  - cybersachet_detailed.ipynb")


if __name__ == "__main__":
    asyncio.run(main())
