#!/usr/bin/env python3
"""
Test overlay functionality on macOS
"""
import tkinter as tk
import time

def test_overlay():
    """Test if we can create a proper overlay"""
    print("Creating test overlay...")
    
    root = tk.Tk()
    root.withdraw()  # Hide main window
    
    # Create overlay
    overlay = tk.Toplevel()
    overlay.attributes('-fullscreen', True)
    overlay.attributes('-alpha', 0.3)
    overlay.configure(bg='black')
    overlay.attributes('-topmost', True)
    overlay.overrideredirect(True)
    
    # Create canvas
    canvas = tk.Canvas(overlay, highlightthickness=0, bg='black', cursor='cross')
    canvas.pack(fill=tk.BOTH, expand=True)
    
    # Add instructions
    instruction_frame = tk.Frame(overlay, bg='yellow', bd=2, relief='raised')
    instruction_frame.pack(pady=20)
    
    instruction_label = tk.Label(instruction_frame, 
                               text="TEST OVERLAY - Click anywhere to close", 
                               bg='yellow', fg='black', font=('Arial', 14, 'bold'), 
                               padx=20, pady=10)
    instruction_label.pack()
    
    def close_overlay(event):
        print("Overlay clicked, closing...")
        overlay.destroy()
        root.quit()
    
    canvas.bind('<Button-1>', close_overlay)
    canvas.focus_set()
    
    print("Overlay created. If you can see this, permissions are OK.")
    print("Click anywhere on the overlay to close it.")
    
    root.mainloop()

if __name__ == "__main__":
    test_overlay()
