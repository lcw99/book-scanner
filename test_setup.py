#!/usr/bin/env python3
"""
Test script to verify the Book Scanner application setup
"""

import sys
import os

def test_imports():
    """Test all required imports"""
    print("Testing imports...")
    
    try:
        import tkinter as tk
        print("✓ tkinter")
    except ImportError as e:
        print(f"✗ tkinter: {e}")
        return False
    
    try:
        from PIL import Image
        print("✓ PIL (Pillow)")
    except ImportError as e:
        print(f"✗ PIL: {e}")
        return False
    
    try:
        import pyautogui
        print("✓ pyautogui")
    except ImportError as e:
        print(f"✗ pyautogui: {e}")
        return False
    
    try:
        import img2pdf
        print("✓ img2pdf")
    except ImportError as e:
        print(f"✗ img2pdf: {e}")
        return False
    
    try:
        import cv2
        print("✓ opencv-python")
    except ImportError as e:
        print(f"✗ opencv-python: {e}")
        return False
    
    try:
        import numpy
        print("✓ numpy")
    except ImportError as e:
        print(f"✗ numpy: {e}")
        return False
    
    try:
        import pdf2image
        print("✓ pdf2image")
    except ImportError as e:
        print(f"✗ pdf2image: {e}")
        return False
    
    try:
        from google.cloud import vision
        print("✓ google-cloud-vision")
    except ImportError as e:
        print(f"✗ google-cloud-vision: {e}")
        return False
    
    return True

def test_gui_creation():
    """Test if GUI can be created"""
    print("\nTesting GUI creation...")
    
    try:
        # Add current directory to path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, current_dir)
        
        from app.book_scanner_gui import BookScannerApp
        import tkinter as tk
        
        # Create a test root window
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        # Try to create the app
        app = BookScannerApp(root)
        print("✓ GUI application created successfully")
        
        # Clean up
        root.destroy()
        return True
        
    except Exception as e:
        print(f"✗ GUI creation failed: {e}")
        return False

def test_screen_capture():
    """Test basic screen capture functionality"""
    print("\nTesting screen capture...")
    
    try:
        import pyautogui
        
        # Test screenshot capability
        screenshot = pyautogui.screenshot()
        print(f"✓ Screen capture successful - Image size: {screenshot.size}")
        return True
        
    except Exception as e:
        print(f"✗ Screen capture failed: {e}")
        return False

def main():
    print("Book Scanner Application Test")
    print("=" * 40)
    
    # Test imports
    if not test_imports():
        print("\n❌ Import test failed - some dependencies are missing")
        return False
    
    # Test GUI creation
    if not test_gui_creation():
        print("\n❌ GUI test failed")
        return False
    
    # Test screen capture
    if not test_screen_capture():
        print("\n❌ Screen capture test failed")
        return False
    
    print("\n" + "=" * 40)
    print("🎉 ALL TESTS PASSED!")
    print("The Book Scanner application is ready to use.")
    print("\nTo run the application:")
    print("  - Execute: ./run_book_scanner.sh")
    print("  - Or run: python3 run_book_scanner.py")
    print("=" * 40)
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
