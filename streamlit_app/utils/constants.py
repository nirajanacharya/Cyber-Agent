"""App constants and configuration."""

# Page configuration
PAGE_TITLE = "Cyber Sachet - Nepal Cyber Security Assistant"
PAGE_ICON = "⚡"
LAYOUT = "wide"

# ChromaDB configuration
COLLECTION_NAME = "cyber_sachet"
EMBEDDING_MODEL = "text-embedding-3-small"
DOCS_FOLDER = "docs/"

# Agent configuration
DEFAULT_MODEL = "gpt-4o-mini"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_N_DOCS = 5

# Monitoring
SERVICE_NAME = "cyber-sachet-streamlit"

# UI Configuration
STREAMING_SPEED = 0.03  # seconds per word
MAX_MESSAGE_LENGTH = 5000

# Custom CSS for professional look
CUSTOM_CSS = """
<style>
    /* Main container styling */
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    
    /* Chat message styling */
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    
    /* Button styling */
    .stButton>button {
        border-radius: 0.25rem;
        font-weight: 500;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        font-weight: 500;
        color: #1f1f1f;
    }
    
    /* Metric styling */
    [data-testid="stMetricValue"] {
        font-size: 1.5rem;
    }
    
    /* Divider styling */
    hr {
        margin: 1.5rem 0;
    }
</style>
"""
