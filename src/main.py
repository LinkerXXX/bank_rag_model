"""
Banking RAG Assistant
"""

import sys
from pathlib import Path

def check_environment():
    
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    print(f"{python_version}")
    
    root = Path(__file__).parent.parent
    required_folders = ["data", "src", "tests"]
    
    for folder in required_folders:
        if (root / folder).exists():
            print(f"{folder}")
        else:
            print(f"Пусто")
    
    print("\n")

if __name__ == "__main__":
    check_environment()
