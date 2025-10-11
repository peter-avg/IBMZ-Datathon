#!/usr/bin/env python3
"""Run script for the AI-assisted Clinical Forms Streamlit application."""

import subprocess
import sys
import os

def main():
    """Run the Streamlit application."""
    # Change to the frontend directory
    frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")
    
    if not os.path.exists(frontend_dir):
        print("Error: Frontend directory not found!")
        sys.exit(1)
    
    # Run streamlit
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "0.0.0.0"
        ], cwd=frontend_dir, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running Streamlit: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nApplication stopped by user.")
        sys.exit(0)

if __name__ == "__main__":
    main()
