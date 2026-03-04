"""Feedback UI component."""

import streamlit as st


class FeedbackWidget:
    """User feedback buttons and collection."""
    
    def __init__(self, feedback_collector, session_id):
        self.collector = feedback_collector
        self.session_id = session_id
    
    def render(self, message: dict):
        """Render feedback buttons for a message."""
        query_id = message.get('query_id')
        if not query_id:
            return
        
        st.markdown("---")
        st.caption("Was this answer helpful?")
        
        col1, col2, col3 = st.columns([1, 1, 6])
        
        with col1:
            if st.button("👍 Yes", key=f"helpful_{query_id}", use_container_width=True):
                self._handle_positive(query_id)
        
        with col2:
            if st.button("👎 No", key=f"not_helpful_{query_id}", use_container_width=True):
                self._handle_negative(query_id)
    
    def _handle_positive(self, query_id: str):
        """Handle positive feedback."""
        self.collector.add_rating(
            self.session_id,
            query_id,
            'positive'
        )
        st.success("Thank you for your feedback!")
    
    def _handle_negative(self, query_id: str):
        """Handle negative feedback."""
        self.collector.add_rating(
            self.session_id,
            query_id,
            'negative'
        )
        st.info("Thank you for your feedback. We're constantly improving!")
