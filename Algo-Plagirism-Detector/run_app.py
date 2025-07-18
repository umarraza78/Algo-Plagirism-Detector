#!/usr/bin/env python3
"""
Script to run the Streamlit app.
"""

import os
import subprocess
import sys

def main():
    """Run the Streamlit app."""
    try:
        # Try to run the app using the streamlit module
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except Exception as e:
        print(f"Error running Streamlit app: {e}")
        print("Please make sure Streamlit is installed:")
        print("pip install streamlit")

if __name__ == "__main__":
    main()
