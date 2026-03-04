

import streamlit as st
import uuid
import sys
import os
from pathlib import Path
from dotenv import load_dotenv


project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from streamlit_app.core import SessionManager
from streamlit_app.core.agent_setup import AgentManager  # Lazy import
from streamlit_app.ui import Header, Sidebar, ChatInterface, FeedbackWidget, Footer
from streamlit_app.ui.welcome import WelcomeMessage
from streamlit_app.utils import PAGE_TITLE, PAGE_ICON, LAYOUT, CUSTOM_CSS


load_dotenv()


st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=LAYOUT,
    initial_sidebar_state="expanded",
    menu_items={
        'About': "Cyber Sachet - Educational tool for Nepal cyber security and cyber law information"
    }
)


st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


@st.cache_resource
def initialize_app():
    """Initialize app components (cached for performance)."""
    manager = AgentManager()
    manager.initialize()
    return manager


def main():
    """Main application entry point."""
    
    manager = initialize_app()
    agent = manager.get_agent()
    tracker = manager.get_tracker()
    feedback_collector = manager.get_feedback_collector()
    
   
    SessionManager.initialize()
    session_id = SessionManager.get_session_id()
    
    
    Header.render()
    
    
    Sidebar.render(
        tracker=tracker,
        session_id=session_id,
        on_clear_chat=lambda: SessionManager.clear_messages() or agent.clear_history()
    )
    
    
    feedback_widget = FeedbackWidget(feedback_collector, session_id)
    
   
    messages = SessionManager.get_messages()
    
    
    if len(messages) == 0:
        WelcomeMessage.render()
    else:
        ChatInterface.render_messages(messages, feedback_widget)
    
   
    user_input = ChatInterface.get_user_input()
    
    if user_input:
      
        SessionManager.add_message("user", user_input)
        ChatInterface.display_user_message(user_input)
        
        
        result = ChatInterface.process_query(agent, user_input, session_id)
        
       
        ChatInterface.display_assistant_message_streaming(result)
        
       
        query_id = str(uuid.uuid4())
        SessionManager.add_message(
            "assistant",
            result['answer'],
            query_id=query_id
        )
        
      
        st.rerun()
    
   
    Footer.render(session_id)


if __name__ == "__main__":
    main()
