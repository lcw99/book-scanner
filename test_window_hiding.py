#!/usr/bin/env python3
"""
Test script to verify window hiding behavior during selection
"""
import sys
import os

# Add app directory to path
app_dir = os.path.join(os.path.dirname(__file__), 'app')
sys.path.insert(0, app_dir)

# Test the book scanner app
from app.book_scanner_gui import main

if __name__ == "__main__":
    print("Testing Book Scanner with window hiding functionality...")
    print("Steps to test:")
    print("1. Click 'Select Page Area' - main window should hide")
    print("2. You should see a transparent overlay")
    print("3. Select an area or press ESC to cancel")
    print("4. Main window should reappear")
    print("5. Click 'Select Next Button' - main window should hide again")
    print("6. Click a location or press ESC to cancel")
    print("7. Main window should reappear")
    print("\nStarting app...")
    main()
