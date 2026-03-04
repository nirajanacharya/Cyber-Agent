"""Chat interface component."""

import streamlit as st
import asyncio
import time
from ..utils import STREAMING_SPEED


class ChatInterface:
    """Manages chat UI and interactions."""
    
    @staticmethod
    def render_messages(messages, feedback_component):
        """Render chat message history."""
        for msg in messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                
               
                if msg["role"] == "assistant" and "query_id" in msg:
                    feedback_component.render(msg)
    
    @staticmethod
    def get_user_input(placeholder: str = "Type your question here...") -> str:
        """Get user input from chat."""
        return st.chat_input(placeholder)
    
    @staticmethod
    def display_user_message(content: str):
        """Display user message."""
        with st.chat_message("user"):
            st.markdown(content)
    
    @staticmethod
    def display_assistant_message_streaming(result: dict):
        """Display assistant message with streaming effect."""
        with st.chat_message("assistant"):
           
            message_placeholder = st.empty()
            
            
            full_response = result['answer']
            displayed_response = ""
            
            
            words = full_response.split()
            
            for i, word in enumerate(words):
                displayed_response += word + " "
                
                message_placeholder.markdown(displayed_response + "▌")
                
                time.sleep(STREAMING_SPEED)
            
          
            message_placeholder.markdown(full_response)
            
            
            if result.get('sources_used'):
                ChatInterface._render_sources(result)
    
    @staticmethod
    def _render_sources(result: dict):
        """Render source citations."""
        with st.expander("View Sources"):
            st.markdown("**References:**")
            for i, source in enumerate(result['sources_used'], 1):
                st.markdown(f"{i}. {source}")
    
    @staticmethod
    def process_query(agent, query: str, session_id: str, verbose: bool = False):
        """Process user query with agent."""
        with st.spinner("Analyzing your question..."):
            result = asyncio.run(agent.query(
                user_question=query,
                session_id=session_id,
                verbose=verbose
            ))
        return result
