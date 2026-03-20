"""Shared setup helpers for evaluation scripts."""

import os
from pathlib import Path

import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
from openai import AsyncOpenAI

from cyber_sachet.agent.agent import create_agent
from cyber_sachet.database.document_loader import load_documents
from cyber_sachet.tools.base import create_tools

ROOT = Path(__file__).resolve().parents[2]
DOCS_DIR = ROOT / "docs"
COLLECTION_NAME = "cyber_sachet_eval"


def create_eval_agent(model_name: str = "text-embedding-3-small"):
    """Initialize and return a CyberSachetAgent for evaluation runs."""
    load_dotenv(ROOT / ".env")
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment")

    client = AsyncOpenAI(api_key=api_key)
    db_client = chromadb.Client()
    embedding_fn = embedding_functions.OpenAIEmbeddingFunction(
        api_key=api_key,
        model_name=model_name,
    )
    collection = db_client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_fn,
    )

    if collection.count() == 0:
        load_documents(collection, str(DOCS_DIR))

    tools = create_tools(collection, embedding_fn, enable_logging=False)
    return create_agent(tools, client)
