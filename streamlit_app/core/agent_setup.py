"""Agent initialization and setup."""

import os
from openai import AsyncOpenAI
import chromadb
from chromadb.utils import embedding_functions
import streamlit as st

from cyber_sachet.tools.base import create_tools
from cyber_sachet.agent.agent import create_agent
from cyber_sachet.database.document_loader import load_documents
from ..utils.constants import (
    COLLECTION_NAME,
    EMBEDDING_MODEL,
    DOCS_FOLDER,
    SERVICE_NAME
)


def get_api_key(key_name: str) -> str:
    """Get API key from Streamlit secrets or environment variables.
    
    This supports both:
    - Streamlit Cloud deployment (uses st.secrets)
    - Local development (uses .env file via os.getenv)
    """
    # Try Streamlit secrets first (for cloud deployment)
    try:
        if hasattr(st, 'secrets'):
            # Try to access the key - may fail if secrets.toml doesn't exist
            return st.secrets[key_name]
    except Exception:
        # FileNotFoundError: secrets.toml missing
        # KeyError: key not in secrets
        pass
    
    # Fall back to environment variable (local development with .env)
    value = os.getenv(key_name)
    if value:
        return value
    
    raise ValueError(
        f"{key_name} not found. "
        f"For local development: add to .env file. "
        f"For Streamlit Cloud: add to app secrets."
    )


class AgentManager:
    """Manages agent initialization and lifecycle."""
    
    def __init__(self):
        self.agent = None
        self.feedback = None
        self.tracker = None
        self._initialized = False
    
    def initialize(self):
        """Initialize all components."""
        if self._initialized:
            return self
        
        
        from monitoring.logfire_config import setup_logfire
        from monitoring.agent_monitor import MonitoredAgent
        from monitoring.feedback_collector import FeedbackCollector
        from monitoring.session_tracker import SessionTracker
        
        
        setup_logfire(SERVICE_NAME)
        
       
        api_key = get_api_key("OPENAI_API_KEY")
        client = AsyncOpenAI(api_key=api_key)
        
      
        db_client = chromadb.Client()
        embedding_fn = embedding_functions.OpenAIEmbeddingFunction(
            api_key=api_key,
            model_name=EMBEDDING_MODEL
        )
        
        collection = db_client.get_or_create_collection(
            name=COLLECTION_NAME,
            embedding_function=embedding_fn
        )
        
       
        if collection.count() == 0:
            load_documents(collection, DOCS_FOLDER)
        
        
        tools = create_tools(collection, embedding_fn)
        base_agent = create_agent(tools, client)
        
        
        self.tracker = SessionTracker()
        self.agent = MonitoredAgent(base_agent, self.tracker)
        self.feedback = FeedbackCollector()
        
        self._initialized = True
        return self
    
    def get_agent(self):
        """Get monitored agent instance."""
        if not self._initialized:
            raise RuntimeError("Agent not initialized. Call initialize() first.")
        return self.agent
    
    def get_tracker(self):
        """Get session tracker."""
        return self.tracker
    
    def get_feedback_collector(self):
        """Get feedback collector."""
        return self.feedback
