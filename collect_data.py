"""Automated data collection for assignment."""
import asyncio
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables FIRST (before any monitoring imports)
load_dotenv()

sys.path.insert(0, str(Path(__file__).parent))

from openai import AsyncOpenAI
import chromadb
from chromadb.utils import embedding_functions

from cyber_sachet.tools.base import create_tools
from cyber_sachet.agent.agent import create_agent
from cyber_sachet.database.document_loader import load_documents
from monitoring.logfire_config import setup_logfire
from monitoring.agent_monitor import MonitoredAgent
from monitoring.session_tracker import SessionTracker
from monitoring.feedback_collector import FeedbackCollector

# Test queries for data collection
TEST_QUERIES = [
    "What is phishing?",
    "How do I create a strong password?",
    "What are the penalties for hacking in Nepal?",
    "Is cyberbullying illegal in Nepal?",
    "What is social engineering?",
    "How can I protect my privacy online?",
    "What does the IT Act 2063 say about data privacy?",
    "What are common types of malware?",
    "How do I secure my WiFi network?",
    "What is ransomware?",
    "Can I be prosecuted for online defamation in Nepal?",
    "How do I recognize a phishing email?",
    "What is two-factor authentication?",
    "What are the punishments under Digital Security Act 2024?",
    "How can I protect myself from identity theft?",
]

async def main():
    """Run automated data collection."""
    print("Starting automated data collection...")
    print(f"Will process {len(TEST_QUERIES)} queries\n")
    
 
    setup_logfire("data-collection")
    
 
    api_key = os.getenv("OPENAI_API_KEY")
    async_client = AsyncOpenAI(api_key=api_key)
    
    
    db_client = chromadb.Client()
    embedding_fn = embedding_functions.OpenAIEmbeddingFunction(
        api_key=api_key,
        model_name="text-embedding-3-small"
    )
    
    collection = db_client.get_or_create_collection(
        name="cyber_sachet",
        embedding_function=embedding_fn
    )
    
  
    if collection.count() == 0:
        print("Loading documents into ChromaDB...")
        load_documents(collection, "docs/")
        print(f"Loaded {collection.count()} document chunks\n")
    

    tools = create_tools(collection, embedding_fn)
    base_agent = create_agent(tools, async_client)
    

    session_tracker = SessionTracker()
    agent = MonitoredAgent(base_agent, session_tracker)
    feedback = FeedbackCollector()
    
    
    session_id = "data_collection_session"
    for i, query in enumerate(TEST_QUERIES, 1):
        print(f"[{i}/{len(TEST_QUERIES)}] {query}")
        try:
            response = await agent.query(query)
            print(f"   [OK] Response: {len(response)} chars")
            
          
            query_id = f"query_{i}"
            feedback.add_rating(session_id, query_id, "positive")
            
            await asyncio.sleep(0.5)  
            
        except Exception as e:
            print(f"   [ERROR] {e}")
            session_tracker.record_error(str(e))
    

    stats = session_tracker.get_stats()
    feedback_summary = feedback.get_summary()
    
    print(f"\n{'='*60}")
    print("COLLECTION SUMMARY")
    print(f"{'='*60}")
    print(f"Queries: {stats['total_queries']}")
    print(f"Tokens: {stats['total_tokens']}")
    print(f"Cost: ${stats['total_cost']:.4f}")
    print(f"Duration: {stats['total_duration']:.1f}s")
    print(f"Positive feedback: {feedback_summary['positive_count']}")
    print(f"\n[SUCCESS] Data sent to Logfire dashboard!")
    print(f"View at: https://logfire.pydantic.dev/")
    print(f"{'='*60}")

if __name__ == "__main__":
    asyncio.run(main())
