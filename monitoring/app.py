"""Streamlit app with monitoring for Cyber Sachet."""

import streamlit as st
import asyncio
import os
import uuid
from dotenv import load_dotenv
from openai import AsyncOpenAI
import chromadb
from chromadb.utils import embedding_functions

from cyber_sachet.tools.base import create_tools
from cyber_sachet.agent.agent import create_agent
from cyber_sachet.database.document_loader import load_documents
from monitoring.logfire_config import setup_logfire
from monitoring.agent_monitor import MonitoredAgent
from monitoring.feedback_collector import FeedbackCollector
from monitoring.session_tracker import SessionTracker


load_dotenv()


st.set_page_config(
    page_title="Cyber Sachet - Nepal Cyber Security",
    page_icon="🛡️",
    layout="wide"
)


@st.cache_resource
def init_agent():
    """Initialize monitored agent."""
    
    setup_logfire("cyber-sachet-app")
    
   
    client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
  
    db_client = chromadb.Client()
    embedding_fn = embedding_functions.OpenAIEmbeddingFunction(
        api_key=os.getenv("OPENAI_API_KEY"),
        model_name="text-embedding-3-small"
    )
    
    collection = db_client.get_or_create_collection(
        name="cyber_sachet",
        embedding_function=embedding_fn
    )
    
    
    if collection.count() == 0:
        load_documents(collection, "docs/")
    
    
    tools = create_tools(collection, embedding_fn)
    base_agent = create_agent(tools, client)
    

    tracker = SessionTracker()
    monitored = MonitoredAgent(base_agent, tracker)
    feedback = FeedbackCollector()
    
    return monitored, feedback, tracker



agent, feedback, tracker = init_agent()


if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if 'messages' not in st.session_state:
    st.session_state.messages = []


st.title("🛡️ Cyber Sachet")
st.markdown("*Your AI assistant for Nepal cyber security*")


with st.sidebar:
    st.header("📊 Session Stats")
    
    stats = tracker.get_stats(st.session_state.session_id)
    
    if stats['queries'] > 0:
        st.metric("Queries", stats['queries'])
        st.metric("Tokens Used", stats['tokens'])
        st.metric("Avg Time", f"{stats['avg_duration']:.0f}ms")
        cost = stats['tokens'] * 0.0000002
        st.metric("Cost", f"${cost:.6f}")
    else:
        st.info("No queries yet")
    
    st.divider()
    
    if st.button("Clear Chat"):
        st.session_state.messages = []
        agent.clear_history()
        st.rerun()


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        
        
        if msg["role"] == "assistant" and "query_id" in msg:
            col1, col2 = st.columns([1, 1])
            
            with col1:
                if st.button("👍", key=f"up_{msg['query_id']}"):
                    feedback.add_rating(
                        st.session_state.session_id,
                        msg['query_id'],
                        'positive'
                    )
                    st.success("Thanks!")
            
            with col2:
                if st.button("👎", key=f"down_{msg['query_id']}"):
                    feedback.add_rating(
                        st.session_state.session_id,
                        msg['query_id'],
                        'negative'
                    )
                    st.warning("We'll improve!")


if prompt := st.chat_input("Ask about cyber security..."):
  
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
   
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = asyncio.run(agent.query(
                user_question=prompt,
                session_id=st.session_state.session_id,
                verbose=False
            ))
            
            st.markdown(result['answer'])
            
           
            with st.expander("📋 Details"):
                st.write(f"**Duration:** {result['monitoring']['duration_ms']:.0f}ms")
                st.write(f"**Tokens:** ~{result['monitoring']['tokens']}")
                st.write(f"**Cost:** ~${result['monitoring']['cost']:.6f}")
                st.write(f"**Tools:** {', '.join(result['tools_used'])}")
                st.write(f"**Sources:** {', '.join(result['sources_used'])}")
            
           
            query_id = str(uuid.uuid4())
            st.session_state.messages.append({
                "role": "assistant",
                "content": result['answer'],
                "query_id": query_id
            })
            
            st.rerun()
