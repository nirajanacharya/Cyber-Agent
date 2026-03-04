"""Footer component."""

import streamlit as st


class Footer:
    """Renders app footer."""
    
    @staticmethod
    def render(session_id: str):
        """Display app footer."""
        st.divider()
        st.markdown("""
        <div style='text-align: center; color: #666; font-size: 0.85em; padding: 20px 0;'>
            <strong>Cyber Sachet</strong> - Nepal Cyber Security & Cyber Law Assistant<br>
            <em>Disclaimer: This tool provides educational information only. For legal advice, please consult qualified legal professionals.</em>
        </div>
        """, unsafe_allow_html=True)
