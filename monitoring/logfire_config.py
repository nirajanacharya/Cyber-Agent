"""Logfire setup and configuration."""

import os
import logfire


def get_logfire_token() -> str:
    """Get Logfire token from Streamlit secrets or environment.
    
    Supports:
    - Streamlit Cloud deployment (st.secrets)
    - Local development (.env file)
    - Direct environment variables
    """
    # Try Streamlit secrets first (for cloud deployment)
    try:
        import streamlit as st
        if hasattr(st, 'secrets'):
            # Try to access the token - may fail if secrets.toml doesn't exist
            return st.secrets['LOGFIRE_TOKEN']
    except (ImportError, Exception):
        # ImportError: Streamlit not available (standalone scripts)
        # FileNotFoundError/KeyError/etc: secrets.toml missing or token not in it
        pass
    
    # Fall back to environment variable (local development with .env)
    token = os.getenv("LOGFIRE_TOKEN")
    if token:
        return token
    
    raise ValueError(
        "LOGFIRE_TOKEN not found. "
        "Add to .env file (local) or Streamlit secrets (cloud)."
    )


def setup_logfire(service_name: str = "cyber-sachet"):
    """Initialize Logfire for monitoring."""
    token = get_logfire_token()
    
    logfire.configure(
        token=token,
        service_name=service_name,
        send_to_logfire=True
    )
    
    logfire.info("Logfire initialized", service=service_name)
    return logfire

