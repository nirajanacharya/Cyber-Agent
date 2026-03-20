

import subprocess
import sys
import os

if __name__ == "__main__":
 
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)
    
    print(" Starting Cyber Sachet Streamlit App...")

    

    subprocess.run([
        sys.executable, "-m", "streamlit", "run",
        "streamlit_app/app.py",
        "--server.headless", "true"
    ])
