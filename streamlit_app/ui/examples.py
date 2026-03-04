"""Example questions component."""

import streamlit as st


class ExampleQuestions:
    """Display example questions to guide users."""
    
    EXAMPLES = [
        "What is the Nepal Information Technology Act 2063?",
        "What are the penalties for hacking in Nepal?",
        "How can I protect myself from phishing attacks?",
        "What is considered cybercrime under Nepal law?",
        "What are best practices for password security?",
        "What does the Digital Security Act 2024 cover?",
    ]
    
    @staticmethod
    def render():
        """Display example questions."""
        st.subheader("Example Questions")
        st.markdown("Try asking questions like:")
        
        for example in ExampleQuestions.EXAMPLES[:4]:
            st.markdown(f"- {example}")
        
        with st.expander("See more examples"):
            for example in ExampleQuestions.EXAMPLES[4:]:
                st.markdown(f"- {example}")
