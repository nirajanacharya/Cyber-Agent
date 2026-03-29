"""Sidebar UI component."""

import streamlit as st
from .examples import ExampleQuestions
from ..utils import truncate_text


class Sidebar:
    """Renders sidebar with stats and info."""
    
    @staticmethod
    def render(tracker, session_id, messages, on_clear_chat):
        """Render sidebar."""
        with st.sidebar:
            Sidebar._render_stats(tracker, session_id)
            st.divider()
            Sidebar._render_history(messages)
            st.divider()
            Sidebar._render_info()
            st.divider()
            ExampleQuestions.render()
            Sidebar._render_actions(on_clear_chat)
    
    @staticmethod
    def _render_stats(tracker, session_id):
        """Render session statistics."""
        st.subheader("Conversation")
        
        stats = tracker.get_stats(session_id)
        
        if stats['queries'] > 0:
            st.metric("Questions in this session", stats['queries'])
        else:
            st.info("Your conversation history will appear here")
    
    @staticmethod
    def _render_info():
        """Render app information."""
        st.subheader("Topics I Can Help With")
        st.markdown("""
        - Nepal's cyber laws and regulations
        - Information Technology Act 2063
        - Digital Security Act 2024
        - Cyber security best practices
        - Legal penalties for cyber crimes
        - Online safety and awareness
        """)

    @staticmethod
    def _render_history(messages):
        """Render recent question history with readable names."""
        st.subheader("Recent Questions")

        user_messages = [msg["content"] for msg in messages if msg.get("role") == "user"]

        if not user_messages:
            st.caption("No questions yet")
            return

        for question in reversed(user_messages[-5:]):
            st.markdown(f"- {truncate_text(question, 60)}")
    
    @staticmethod
    def _render_actions(on_clear_chat):
        """Render action buttons."""
        st.divider()
        
        if st.button("Start New Conversation", use_container_width=True, type="primary"):
            on_clear_chat()
            st.rerun()
