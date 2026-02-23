"""PyTest fixtures for Cyber Sachet tests."""

import pytest
import asyncio
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
import chromadb
from chromadb.utils import embedding_functions
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from cyber_sachet.tools.base import create_tools
from cyber_sachet.agent.agent import create_agent


@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for the session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def openai_client():
    """Create OpenAI client."""
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        pytest.skip("OPENAI_API_KEY not set")
    return AsyncOpenAI(api_key=api_key)


@pytest.fixture(scope="session")
def chroma_collection():
    """Create and populate ChromaDB collection."""
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    
    client = chromadb.Client()
    
    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=api_key,
        model_name="text-embedding-3-small"
    )
    
    collection = client.get_or_create_collection(
        name="cyber_sachet_test",
        embedding_function=openai_ef
    )
    
    if collection.count() == 0:
        docs_path = Path(__file__).parent.parent / "docs"
        
        if not docs_path.exists():
            pytest.skip(f"docs folder not found at {docs_path}")
        
        documents = []
        metadatas = []
        ids = []
        
        for doc_file in docs_path.glob("*.txt"):
            with open(doc_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            chunks = [chunk.strip() for chunk in content.split('\n\n') if chunk.strip()]
            
            for i, chunk in enumerate(chunks):
                if len(chunk) > 50:
                    documents.append(chunk)
                    metadatas.append({
                        "source": doc_file.name,
                        "chunk_id": i,
                        "doc_type": "cyber_law" if "act" in doc_file.name.lower() else "awareness"
                    })
                    ids.append(f"{doc_file.stem}_chunk_{i}")
        
        if documents:
            collection.add(documents=documents, metadatas=metadatas, ids=ids)
    
    return collection


@pytest.fixture
def tools(chroma_collection):
    """Create tools instance."""
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=api_key,
        model_name="text-embedding-3-small"
    )
    return create_tools(chroma_collection, openai_ef, enable_logging=True)


@pytest.fixture
def agent(tools, openai_client):
    """Create agent instance."""
    return create_agent(tools, openai_client)
