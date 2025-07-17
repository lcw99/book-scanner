"""
Selection Handlers Module for Book Scanner
Contains all area and button selection functionality
"""
import tkinter as tk
from tkinter import messagebox
import time
import pyautogui
from PIL import Image, ImageTk
import platform
import os


class SelectionHandlers:
    """Handles all selection functionality for area and button selection"""
    
    def __init__(self, app_instance):
        self.app = app_instance
        # Detect if we're on macOS for coordinate adjustments
        self.is_macos = platform.system() == 'Darwin'
        self.scale_factor = 1.0
        if self.is_macos:
            self.app.log_message("macOS detected - using macOS coordinate handling")
            self._get_macos_scale_factor()

    def _get_macos_scale_factor(self):
        """Check for Retina display and get scale factor using tkinter."""
        try:
            # On Retina, this will be 2.0. On non-Retina, 1.0.
            self.scale_factor = float(self.app.root.winfo_pixels('1'))
            if self.scale_factor > 1:
                self.app.log_message(f"Retina display detected with scale factor: {self.scale_factor}")
        except Exception as e:
            self.app.log_message(f"Could not detect screen scale factor, defaulting to 1.0. Error: {e}")
            self.scale_factor = 1.0
        
    def _adjust_coordinates_for_macos(self, x, y):
        """Adjust coordinates for macOS menu bar and Retina scaling."""
        # For now, just return the original coordinates without any adjustment
        # This will help isolate whether the coordinate adjustments are causing the problem
        self.app.log_message(f"Using raw coordinates without adjustment: ({x}, {y})")
        return x, y
    
    def _get_macos_menu_bar_height(self):
        """Get the height of macOS menu bar in points."""
        if self.is_macos:
            # macOS menu bar is typically around 25 points high on most systems
            # Using a fixed value is more reliable since detection methods can be inconsistent
            standard_menu_bar_height = 25
            self.app.log_message(f"Using standard macOS menu bar height: {standard_menu_bar_height} points")
            return standard_menu_bar_height
        return 0

    def select_capture_area(self):
        """Start area selection process - use overlay method"""
        self.app.log_message("Starting overlay area selection...")
        # Use the overlay selection method
        self.create_area_selector()
        
    def create_area_selector(self):
        """Create a transparent overlay for area selection - macOS optimized"""
        overlay = tk.Toplevel()
        
        # Get screen dimensions
        screen_width = overlay.winfo_screenwidth()
        screen_height = overlay.winfo_screenheight()
        
        # Configure overlay to cover full screen
        overlay.geometry(f"{screen_width}x{screen_height}+0+0")
        overlay.configure(bg='black')
        overlay.attributes('-topmost', True)
        overlay.overrideredirect(True)
        overlay.attributes('-alpha', 0.3)
        
        # Ensure overlay gets focus
        overlay.focus_force()
        overlay.grab_set()
        
        # Variables for selection
        start_x = start_y = 0
        rect_id = None
        selecting = False
        
        canvas = tk.Canvas(overlay, highlightthickness=0, bg='black', cursor='cross')
        canvas.pack(fill=tk.BOTH, expand=True)
        
        def start_selection(event):
            nonlocal start_x, start_y, rect_id, selecting
            selecting = True
            start_x, start_y = event.x, event.y
            if rect_id:
                canvas.delete(rect_id)
            print(f"Selection started at: {start_x}, {start_y}")
                
        def update_selection(event):
            nonlocal rect_id, selecting
            if not selecting:
                return
            if rect_id:
                canvas.delete(rect_id)
            rect_id = canvas.create_rectangle(start_x, start_y, event.x, event.y, 
                                            outline='red', width=4, fill='', 
                                            dash=(5, 5))
            canvas.update()
            
        def end_selection(event):
            nonlocal rect_id, selecting
            if not selecting:
                return
            selecting = False
            
            if rect_id:
                canvas.delete(rect_id)
            
            # Calculate selection coordinates relative to canvas
            canvas_x1, canvas_y1 = min(start_x, event.x), min(start_y, event.y)
            canvas_x2, canvas_y2 = max(start_x, event.x), max(start_y, event.y)
            
            # Convert canvas coordinates to absolute screen coordinates
            # Get the absolute position of the overlay window
            overlay_x = overlay.winfo_rootx()
            overlay_y = overlay.winfo_rooty()
            
            # Convert to absolute screen coordinates
            x1 = overlay_x + canvas_x1
            y1 = overlay_y + canvas_y1
            x2 = overlay_x + canvas_x2
            y2 = overlay_y + canvas_y2
            
            # Debug: Log both canvas and screen coordinates 
            self.app.log_message(f"Canvas coordinates: ({canvas_x1}, {canvas_y1}) to ({canvas_x2}, {canvas_y2})")
            self.app.log_message(f"Overlay position: ({overlay_x}, {overlay_y})")
            self.app.log_message(f"Screen coordinates: ({x1}, {y1}) to ({x2}, {y2})")
            
            # Make sure we have a valid selection
            if abs(x2 - x1) < 10 or abs(y2 - y1) < 10:
                overlay.destroy()
                self.app.root.deiconify()
                self.app.log_message("Selection too small, please try again")
                return
            
            # Store the absolute screen coordinates
            self.app.top_left = (x1, y1)
            self.app.bottom_right = (x2, y2)
            
            # Store overlay for further reference
            self.overlay = overlay
            
            # Don't destroy the overlay yet
            overlay.withdraw()  # Just hide it temporarily
            self.app.root.deiconify()  # Show main window again
            
            # Log detailed coordinate information for debugging
            self.app.area_status_label.config(text=f"Area: {self.app.top_left} to {self.app.bottom_right}", foreground="green")
            self.app.log_message(f"Capture area selected (raw): {self.app.top_left} to {self.app.bottom_right}")
            self.app.log_message(f"Selection width: {x2 - x1}, height: {y2 - y1}")
            
            # Take a quick test screenshot with these coordinates
            test_region = (x1, y1, x2 - x1, y2 - y1)
            self.app.log_message(f"Test region for pyautogui: {test_region}")
            try:
                # Take test screenshot and save to desktop
                test_shot = pyautogui.screenshot(region=test_region)
                desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
                test_file = os.path.join(desktop_path, "test_capture_raw.png")
                test_shot.save(test_file)
                self.app.log_message(f"Raw test capture saved to: {test_file}")
                self.app.log_message(f"Please check this image and confirm if it shows the correct area.")
                self.app.log_message(f"Note: If it's correct, you can use 'Test Capture' button to verify again.")
                
                # Now we can destroy the overlay
                overlay.destroy()
                
                # Auto-save settings when area is selected
                if hasattr(self.app, 'settings_manager'):
                    self.app.settings_manager.auto_save_on_selection()
                    
            except Exception as e:
                # Show the overlay again if there was an error
                overlay.destroy()
                self.app.log_message(f"Test screenshot failed: {e}")
            
        def cancel_selection(event=None):
            overlay.destroy()
            self.app.root.deiconify()
            self.app.log_message("Area selection cancelled")
            
        canvas.bind('<Button-1>', start_selection)
        canvas.bind('<B1-Motion>', update_selection)
        canvas.bind('<ButtonRelease-1>', end_selection)
        canvas.bind('<Escape>', cancel_selection)  # Allow escape to cancel
        canvas.bind('<Key>', lambda e: cancel_selection() if e.keysym == 'Escape' else None)
        canvas.focus_set()  # Enable keyboard events
        
        # Instructions - make them more visible and add tips for macOS
        instruction_frame = tk.Frame(overlay, bg='yellow', bd=3, relief='raised')
        instruction_frame.pack(pady=30)
        
        instruction_label = tk.Label(instruction_frame, 
                                   text="DRAG to select the book page area\nPress ESC to cancel\n\nIf screen appears all gray, check macOS Privacy settings", 
                                   bg='yellow', fg='black', font=('Arial', 12, 'bold'), 
                                   padx=20, pady=15, justify='center')
        instruction_label.pack()
        
        # Add a tip for macOS users
        tip_frame = tk.Frame(overlay, bg='orange', bd=2, relief='raised')
        tip_frame.pack(side='bottom', pady=20)
        
        tip_label = tk.Label(tip_frame,
                           text="macOS: Go to System Preferences > Security & Privacy > Privacy\nAdd Python to 'Screen Recording' permissions",
                           bg='orange', fg='black', font=('Arial', 10),
                           padx=15, pady=10, justify='center')
        tip_label.pack()
        
        print("Area selector created. Waiting for user selection...")
            
    def select_next_button(self):
        """Start next button selection process - use overlay method"""
        self.app.log_message("Starting overlay button selection...")
        # Use the overlay selection method
        self.create_button_selector()
        
    def create_button_selector(self):
        """Create a transparent overlay for button selection - same as area selector"""
        overlay = tk.Toplevel()
        
        # Get screen dimensions
        screen_width = overlay.winfo_screenwidth()
        screen_height = overlay.winfo_screenheight()
        
        # Configure overlay for macOS
        overlay.geometry(f"{screen_width}x{screen_height}+0+0")
        overlay.configure(bg='blue')  # Different color to distinguish from area selection
        overlay.attributes('-topmost', True)
        overlay.overrideredirect(True)
        overlay.attributes('-alpha', 0.3)
        
        # Ensure overlay gets focus
        overlay.focus_force()
        overlay.grab_set()
        
        canvas = tk.Canvas(overlay, highlightthickness=0, bg='blue', cursor='crosshair')
        canvas.pack(fill=tk.BOTH, expand=True)
        
        # Add a crosshair that follows the mouse
        crosshair_id = None
        
        def update_crosshair(event):
            nonlocal crosshair_id
            if crosshair_id:
                canvas.delete(crosshair_id)
            
            # Draw crosshair lines
            canvas.create_line(event.x - 20, event.y, event.x + 20, event.y, 
                             fill='red', width=3, tags='crosshair')
            canvas.create_line(event.x, event.y - 20, event.x, event.y + 20, 
                             fill='red', width=3, tags='crosshair')
            crosshair_id = True
        
        def capture_click(event):
            # Convert canvas coordinates to absolute screen coordinates
            overlay_x = overlay.winfo_rootx()
            overlay_y = overlay.winfo_rooty()
            
            # Get absolute screen coordinates
            screen_x = overlay_x + event.x
            screen_y = overlay_y + event.y
            
            self.app.next_button_pos = (screen_x, screen_y)
            
            overlay.destroy()
            self.app.root.deiconify()
            
            self.app.button_status_label.config(text=f"Button at: {self.app.next_button_pos}", foreground="green")
            self.app.log_message(f"Canvas click at: ({event.x}, {event.y})")
            self.app.log_message(f"Overlay position: ({overlay_x}, {overlay_y})")
            self.app.log_message(f"Next button position (screen): {self.app.next_button_pos}")
            
            # Auto-save settings when button is selected
            if hasattr(self.app, 'settings_manager'):
                self.app.settings_manager.auto_save_on_selection()
            
        def cancel_selection(event=None):
            overlay.destroy()
            self.app.root.deiconify()
            self.app.log_message("Button selection cancelled")
            
        canvas.bind('<Motion>', update_crosshair)
        canvas.bind('<Button-1>', capture_click)
        canvas.bind('<Escape>', cancel_selection)
        canvas.bind('<Key>', lambda e: cancel_selection() if e.keysym == 'Escape' else None)
        canvas.focus_set()
        
        # Instructions - make them more visible
        instruction_frame = tk.Frame(overlay, bg='yellow', bd=3, relief='raised')
        instruction_frame.pack(pady=30)
        
        instruction_label = tk.Label(instruction_frame, 
                                   text="CLICK on the next page button location\nPress ESC to cancel\n\nMove mouse to see crosshair", 
                                   bg='yellow', fg='black', font=('Arial', 12, 'bold'), 
                                   padx=20, pady=15, justify='center')
        instruction_label.pack()
        
        # Add a tip for macOS users
        tip_frame = tk.Frame(overlay, bg='orange', bd=2, relief='raised')
        tip_frame.pack(side='bottom', pady=20)
        
        tip_label = tk.Label(tip_frame,
                           text="macOS: Make sure Python has Screen Recording permissions\nif you see a gray screen",
                           bg='orange', fg='black', font=('Arial', 10),
                           padx=15, pady=10, justify='center')
        tip_label.pack()
        
        print("Button selector created. Waiting for user click...")
