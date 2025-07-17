#!/usr/bin/env python3
"""
Simple launcher for Book Scanner (without conda dependency)
Use this if you have the required packages installed in your current Python environment
"""

import sys
import os

def main():
    """Simple launcher that adds app directory to path and runs the application"""
    # Add app directory to Python path
    app_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app')
    sys.path.insert(0, app_dir)
    
    try:
        print("Starting Book Scanner...")
        from book_scanner_gui import main as app_main
        app_main()
    except ImportError as e:
        print(f"Import error: {e}")
        print("\nMissing dependencies. Please install required packages:")
        print("pip install tkinter pillow pyautogui img2pdf pdf2image google-cloud-vision opencv-python")
        print("\nOr use conda environment:")
        print("python run_book_scanner.py")
    except Exception as e:
        print(f"Error starting application: {e}")

if __name__ == "__main__":
    main()
