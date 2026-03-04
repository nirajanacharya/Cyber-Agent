"""Demo script for monitored agent."""

import asyncio
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
import chromadb
from chromadb.utils import embedding_functions

from cyber_sachet.tools.base import create_tools
from cyber_sachet.agent.agent import create_agent
from cyber_sachet.database.document_loader import load_documents
from monitoring.logfire_config import setup_logfire
from monitoring.agent_monitor import MonitoredAgent
from monitoring.feedback_collector import FeedbackCollector


async def main():
    """Run monitoring demo."""
    load_dotenv()
    
    print("🔧 Setting up Logfire...")
    setup_logfire("cyber-sachet-demo")
    
    print("🤖 Initializing agent...")
    client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    db_client = chromadb.Client()
    embedding_fn = embedding_functions.OpenAIEmbeddingFunction(
        api_key=os.getenv("OPENAI_API_KEY"),
        model_name="text-embedding-3-small"
    )
    
    collection = db_client.get_or_create_collection(
        name="cyber_sachet",
        embedding_function=embedding_fn
    )
    
    if collection.count() == 0:
        print("📚 Loading documents...")
        load_documents(collection, "docs/")
    
    tools = create_tools(collection, embedding_fn)
    base_agent = create_agent(tools, client)
    
    monitored_agent = MonitoredAgent(base_agent)
    feedback = FeedbackCollector()
    
    print("\n" + "="*70)
    print("MONITORING DEMO")
    print("="*70)
    
    # Test queries
    queries = [
        "What is phishing?",
        "What are penalties for hacking in Nepal?",
        "How to create a strong password?"
    ]
    
    session_id = "demo_001"
    
    for i, query in enumerate(queries, 1):
        print(f"\n\n🔍 Query {i}: {query}")
        print("-" * 70)
        
        result = await monitored_agent.query(
            user_question=query,
            session_id=session_id,
            verbose=True,
            n_context_docs=3
        )
        
        print(f"\n💬 Answer: {result['answer'][:200]}...")
        print(f"\n📊 Monitoring:")
        print(f"  • Duration: {result['monitoring']['duration_ms']:.0f}ms")
        print(f"  • Tokens: ~{result['monitoring']['tokens']}")
        print(f"  • Cost: ~${result['monitoring']['cost']:.6f}")
        print(f"  • Tools: {', '.join(result['tools_used'])}")
        
      
        if i % 2 == 0:
            feedback.add_rating(session_id, f"q{i}", 'positive')
        
        await asyncio.sleep(1)
    
  
    print("\n\n" + "="*70)
    print("SESSION SUMMARY")
    print("="*70)
    
    stats = monitored_agent.get_session_stats(session_id)
    print(f"Total queries: {stats['queries']}")
    print(f"Total tokens: {stats['tokens']}")
    print(f"Avg time: {stats['avg_duration']:.0f}ms")
    print(f"Total cost: ${stats['tokens'] * 0.0000002:.6f}")
    
    summary = feedback.get_summary()
    print(f"\nFeedback: {summary['positive']}/{summary['total']} positive ({summary['positive_rate']}%)")
    
    print("\n Check Logfire dashboard for detailed traces!")


if __name__ == "__main__":
    asyncio.run(main())
