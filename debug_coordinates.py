#!/usr/bin/env python3
"""
Debug script to check coordinate system and screen capture behavior on macOS
"""
import pyautogui
import tkinter as tk
import platform
import os

def check_macos_coordinates():
    """Check macOS coordinate system and potential offsets"""
    print(f"Platform: {platform.system()} {platform.release()}")
    print(f"pyautogui version: {pyautogui.__version__}")
    
    # Get screen size
    screen_size = pyautogui.size()
    print(f"Screen size: {screen_size}")
    
    # Test screenshot
    try:
        full_screenshot = pyautogui.screenshot()
        print(f"Full screenshot size: {full_screenshot.size}")
        
        # Test a small region
        test_region = (100, 100, 200, 200)
        region_screenshot = pyautogui.screenshot(region=test_region)
        print(f"Region screenshot size: {region_screenshot.size}")
        print(f"Test region: {test_region}")
        
        # Save test files
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        full_screenshot.save(os.path.join(desktop_path, "debug_full_screenshot.png"))
        region_screenshot.save(os.path.join(desktop_path, "debug_region_screenshot.png"))
        print(f"Debug screenshots saved to Desktop")
        
    except Exception as e:
        print(f"Screenshot error: {e}")
    
    # Check failsafe
    print(f"Failsafe enabled: {pyautogui.FAILSAFE}")
    
    # Create a simple GUI to test overlay coordinates
    root = tk.Tk()
    root.title("Coordinate Test")
    root.geometry("300x200+500+300")  # Position window at 500,300
    
    def on_click(event):
        # Get window position
        x = root.winfo_rootx()
        y = root.winfo_rooty()
        print(f"Window position: ({x}, {y})")
        print(f"Click position relative to window: ({event.x}, {event.y})")
        print(f"Calculated screen position: ({x + event.x}, {y + event.y})")
        
        # Test screenshot at click position
        try:
            click_region = (x + event.x - 10, y + event.y - 10, 20, 20)
            click_screenshot = pyautogui.screenshot(region=click_region)
            click_screenshot.save(os.path.join(desktop_path, "debug_click_region.png"))
            print(f"Click region screenshot saved: {click_region}")
        except Exception as e:
            print(f"Click region screenshot failed: {e}")
    
    root.bind("<Button-1>", on_click)
    
    label = tk.Label(root, text="Click anywhere in this window\nto test coordinates", 
                     font=("Arial", 12), pady=50)
    label.pack()
    
    print("\nClick in the window to test coordinate mapping...")
    root.mainloop()

if __name__ == "__main__":
    check_macos_coordinates()
