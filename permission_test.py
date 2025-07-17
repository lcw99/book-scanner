#!/usr/bin/env python3
"""
Test macOS permissions and screen overlay
"""
import tkinter as tk
from tkinter import messagebox
import pyautogui
import time

def test_screen_permissions():
    """Test if we have screen recording permissions"""
    try:
        print("Testing screen capture permissions...")
        test_screenshot = pyautogui.screenshot(region=(0, 0, 100, 100))
        print("✓ Screen recording permissions OK")
        return True
    except Exception as e:
        print(f"✗ Screen recording permission issue: {e}")
        return False

def test_overlay():
    """Test overlay creation"""
    root = tk.Tk()
    root.title("Permission Test")
    root.geometry("300x200")
    
    def start_test():
        print("Creating overlay...")
        root.withdraw()
        
        overlay = tk.Toplevel()
        overlay.geometry("800x600+100+100")  # Don't use fullscreen initially
        overlay.configure(bg='black')
        overlay.attributes('-topmost', True)
        overlay.attributes('-alpha', 0.5)
        
        canvas = tk.Canvas(overlay, bg='black', cursor='cross')
        canvas.pack(fill=tk.BOTH, expand=True)
        
        # Instructions
        instruction = tk.Label(overlay, text="TEST OVERLAY\nClick anywhere to close", 
                             bg='yellow', fg='black', font=('Arial', 14, 'bold'))
        instruction.pack(pady=20)
        
        def close_test(event=None):
            overlay.destroy()
            root.deiconify()
            print("Test completed")
        
        canvas.bind('<Button-1>', close_test)
        overlay.bind('<Escape>', close_test)
        canvas.focus_set()
        
        print("Overlay created. If you see a black window, permissions are working.")
    
    # Test permissions first
    if not test_screen_permissions():
        messagebox.showwarning("Permission Required", 
                             "Screen recording permission is required.\n\n"
                             "Please go to:\n"
                             "System Preferences > Security & Privacy > Privacy > Screen Recording\n"
                             "and add Python to the allowed applications.\n\n"
                             "Then restart this application.")
        root.quit()
        return
    
    tk.Label(root, text="Permission Test", font=("Arial", 16)).pack(pady=20)
    tk.Button(root, text="Test Overlay", command=start_test, font=("Arial", 12)).pack(pady=10)
    tk.Label(root, text="This will test if overlays work correctly", 
             font=("Arial", 10)).pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    test_overlay()
