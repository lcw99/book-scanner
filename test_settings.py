#!/usr/bin/env python3
"""
Test script for the settings functionality
"""
import sys
import os

# Add app directory to path
app_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app')
sys.path.insert(0, app_dir)

try:
    from settings_manager import SettingsManager
    
    # Mock app object for testing
    class MockApp:
        def __init__(self):
            self.top_left = (100, 100)
            self.bottom_right = (500, 400)
            self.next_button_pos = (600, 50)
            self.pages_var = MockVar("15")
            
        def log_message(self, msg):
            print(f"[LOG] {msg}")
    
    class MockVar:
        def __init__(self, value):
            self.value = value
            
        def get(self):
            return self.value
            
        def set(self, value):
            self.value = value
    
    print("=== Testing Settings Manager ===")
    
    # Create mock app and settings manager
    app = MockApp()
    settings_manager = SettingsManager(app)
    
    print("\n1. Testing save_settings()...")
    result = settings_manager.save_settings()
    print(f"Save result: {result}")
    
    print("\n2. Testing load_settings()...")
    # Reset values
    app.top_left = None
    app.bottom_right = None
    app.next_button_pos = None
    app.pages_var.set("10")
    
    result = settings_manager.load_settings()
    print(f"Load result: {result}")
    print(f"Restored top_left: {app.top_left}")
    print(f"Restored bottom_right: {app.bottom_right}")
    print(f"Restored next_button_pos: {app.next_button_pos}")
    print(f"Restored pages: {app.pages_var.get()}")
    
    print("\n3. Testing auto_save_on_selection()...")
    settings_manager.auto_save_on_selection()
    
    print("\n4. Checking settings file...")
    settings_file = os.path.join(app_dir, 'book_scanner_settings.json')
    if os.path.exists(settings_file):
        print(f"Settings file exists: {settings_file}")
        with open(settings_file, 'r') as f:
            content = f.read()
            print(f"Content: {content}")
    else:
        print("Settings file not found")
    
    print("\n=== Settings Manager Test Complete ===")
    
except Exception as e:
    print(f"Error testing settings: {e}")
    import traceback
    traceback.print_exc()
