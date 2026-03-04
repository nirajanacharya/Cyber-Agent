"""Quick run script for Streamlit app."""

import subprocess
import sys
import os

if __name__ == "__main__":
    # Ensure we're in the right directory
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)
    
    print("🚀 Starting Cyber Sachet Streamlit App...")
    print("=" * 70)
    
    # Run streamlit
    subprocess.run([
        sys.executable, "-m", "streamlit", "run",
        "streamlit_app/app.py",
        "--server.headless", "true"
    ])
