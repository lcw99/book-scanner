#!/usr/bin/env python3
"""
Quick test script to verify the GUI integration with async OCR works
"""

import tkinter as tk
from tkinter import messagebox
import os
import sys

# Add app directory to path
app_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app')
sys.path.insert(0, app_dir)

def test_gui():
    """Test the book scanner GUI with async OCR functionality"""
    try:
        from book_scanner_gui import BookScannerApp
        
        print("🚀 Starting Book Scanner GUI Test...")
        print("📋 Testing new async OCR functionality...")
        
        root = tk.Tk()
        app = BookScannerApp(root)
        
        # Add a test message to verify the GUI loads
        app.log_message("🔥 GUI Test Mode - Async OCR Ready!")
        app.log_message("✨ New features:")
        app.log_message("   • Choose between Traditional and Async OCR methods")
        app.log_message("   • Async method uses Google Cloud Storage for faster processing")
        app.log_message("   • Bucket configured: book-scanner-ocr-bucket")
        app.log_message("")
        app.log_message("📝 To test:")
        app.log_message("   1. Click 'Select PDF & Extract Text'")
        app.log_message("   2. Choose OCR method when prompted")
        app.log_message("   3. Select a PDF file to process")
        app.log_message("")
        
        print("✅ GUI loaded successfully!")
        print("🖱️  Click 'Select PDF & Extract Text' button to test async OCR")
        
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Error loading GUI: {e}")
        messagebox.showerror("Error", f"Failed to load GUI: {e}")

if __name__ == "__main__":
    test_gui()
