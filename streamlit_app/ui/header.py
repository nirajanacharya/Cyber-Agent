"""Header component."""

import streamlit as st


class Header:
    """Renders app header."""
    
    @staticmethod
    def render():
        """Display app title and description."""
        st.title("Cyber Sachet")
        st.subheader("Nepal Cyber Security & Cyber Law Assistant")
        st.markdown("""
        Get informed answers about Nepal's cyber laws, security best practices, 
        and legal implications of cyber activities. 
        """)
        st.divider()
