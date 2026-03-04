"""Welcome message component."""

import streamlit as st


class WelcomeMessage:
    """Display welcome message for new users."""
    
    @staticmethod
    def render():
        """Display welcome card."""
        st.info("""
        **Welcome to Cyber Sachet!**
        
        I'm here to help you understand Nepal's cyber laws and security best practices. 
        You can ask me about:
        
        - Legal aspects of cyber activities in Nepal
        - Penalties and consequences for cyber crimes
        - How to stay safe online
        - Understanding the IT Act 2063 and Digital Security Act 2024
        
        Ask your first question below to get started!
        """)
