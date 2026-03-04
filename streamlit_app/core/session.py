"""Session state management."""

import streamlit as st
import uuid


class SessionManager:
    """Manages Streamlit session state."""
    
    @staticmethod
    def initialize():
        """Initialize session state variables."""
        if 'session_id' not in st.session_state:
            st.session_state.session_id = str(uuid.uuid4())
        
        if 'messages' not in st.session_state:
            st.session_state.messages = []
    
    @staticmethod
    def get_session_id() -> str:
        """Get current session ID."""
        return st.session_state.session_id
    
    @staticmethod
    def get_messages() -> list:
        """Get chat messages."""
        return st.session_state.messages
    
    @staticmethod
    def add_message(role: str, content: str, **kwargs):
        """Add message to chat history."""
        message = {"role": role, "content": content, **kwargs}
        st.session_state.messages.append(message)
    
    @staticmethod
    def clear_messages():
        """Clear all messages."""
        st.session_state.messages = []
    
    @staticmethod
    def get_message_count() -> int:
        """Get number of messages."""
        return len(st.session_state.messages)
