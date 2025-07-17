"""
GUI Components Module for Book Scanner
Contains all GUI creation and layout functionality
"""
import tkinter as tk
from tkinter import ttk
import os
import subprocess
import platform


class GUIComponents:
    """Handles all GUI creation and layout for the Book Scanner application"""
    
    def __init__(self, app_instance):
        self.app = app_instance
        
    def create_widgets(self):
        """Create all GUI widgets and layout"""
        # Main frame
        main_frame = ttk.Frame(self.app.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Book Scanner", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Step 1: Select capture area
        self._create_step1_frame(main_frame)
        
        # Step 2: Select next button
        self._create_step2_frame(main_frame)
        
        # Step 3: Set page count
        self._create_step3_frame(main_frame)
        
        # Step 4: Capture and Process
        self._create_step4_frame(main_frame)
        
        # PDF OCR section
        self._create_pdf_ocr_frame(main_frame)
        
        # Progress section
        self._create_progress_frame(main_frame)
        
        # Output section
        self._create_output_frame(main_frame)
        
        # Configure grid weights
        self._configure_grid_weights(main_frame)
        
    def _create_step1_frame(self, parent):
        """Create Step 1 frame for area selection"""
        step1_frame = ttk.LabelFrame(parent, text="Step 1: Select Book Page Area", padding="10")
        step1_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(step1_frame, text="Click the button below, then drag to select the book page area on your screen.").grid(row=0, column=0, columnspan=2, sticky=tk.W)
        
        self.app.select_area_btn = ttk.Button(step1_frame, text="Select Page Area", command=self.app.select_capture_area)
        self.app.select_area_btn.grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        
        # Add test capture button to verify coordinates
        self.app.test_capture_btn = ttk.Button(step1_frame, text="Test Capture", command=self.app.test_capture_area)
        self.app.test_capture_btn.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=(10, 0))
        
        self.app.area_status_label = ttk.Label(step1_frame, text="No area selected", foreground="red")
        self.app.area_status_label.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(10, 0))
        
    def _create_step2_frame(self, parent):
        """Create Step 2 frame for button selection"""
        step2_frame = ttk.LabelFrame(parent, text="Step 2: Select Next Page Button", padding="10")
        step2_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(step2_frame, text="Click the button below, then click on the 'Next Page' button location.").grid(row=0, column=0, columnspan=2, sticky=tk.W)
        
        self.app.select_button_btn = ttk.Button(step2_frame, text="Select Next Button", command=self.app.select_next_button)
        self.app.select_button_btn.grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        
        self.app.button_status_label = ttk.Label(step2_frame, text="No button selected", foreground="red")
        self.app.button_status_label.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(10, 0))
        
    def _create_step3_frame(self, parent):
        """Create Step 3 frame for page count"""
        step3_frame = ttk.LabelFrame(parent, text="Step 3: Set Total Pages", padding="10")
        step3_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(step3_frame, text="Enter the total number of pages to capture:").grid(row=0, column=0, sticky=tk.W)
        
        self.app.pages_var = tk.StringVar(value="10")
        self.app.pages_entry = ttk.Entry(step3_frame, textvariable=self.app.pages_var, width=10)
        self.app.pages_entry.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
    def _create_step4_frame(self, parent):
        """Create Step 4 frame for capture and process"""
        step4_frame = ttk.LabelFrame(parent, text="Step 4: Capture and Process", padding="10")
        step4_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.app.capture_btn = ttk.Button(step4_frame, text="Start Capture & OCR", command=self.app.start_capture_process)
        self.app.capture_btn.grid(row=0, column=0, sticky=tk.W)
        
        self.app.stop_btn = ttk.Button(step4_frame, text="Stop", command=self.app.stop_capture, state="disabled")
        self.app.stop_btn.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        self.app.open_folder_btn = ttk.Button(step4_frame, text="Open Output Folder", command=self.open_output_folder)
        self.app.open_folder_btn.grid(row=0, column=2, sticky=tk.W, padx=(10, 0))
        
    def _create_pdf_ocr_frame(self, parent):
        """Create PDF OCR frame for processing existing PDFs"""
        pdf_ocr_frame = ttk.LabelFrame(parent, text="OCR Existing PDF", padding="10")
        pdf_ocr_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(pdf_ocr_frame, text="Already have a PDF? Extract text using OCR:").grid(row=0, column=0, columnspan=2, sticky=tk.W)
        
        self.app.process_pdf_btn = ttk.Button(pdf_ocr_frame, text="Select PDF & Extract Text", command=self.app.process_existing_pdf)
        self.app.process_pdf_btn.grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        
        # Settings section
        self._create_settings_frame(parent)
        
    def _create_settings_frame(self, parent):
        """Create settings management frame"""
        settings_frame = ttk.LabelFrame(parent, text="Settings", padding="10")
        settings_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(settings_frame, text="Area and button positions are automatically saved and restored on startup.").grid(row=0, column=0, columnspan=3, sticky=tk.W)
        
        # Settings buttons
        self.app.save_settings_btn = ttk.Button(settings_frame, text="Save Settings", command=self.save_settings_manually)
        self.app.save_settings_btn.grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        
        self.app.clear_settings_btn = ttk.Button(settings_frame, text="Clear Settings", command=self.clear_settings)
        self.app.clear_settings_btn.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=(5, 0))
        
        self.app.reset_selections_btn = ttk.Button(settings_frame, text="Reset Selections", command=self.reset_selections)
        self.app.reset_selections_btn.grid(row=1, column=2, sticky=tk.W, padx=(10, 0), pady=(5, 0))
        
        self.app.show_status_btn = ttk.Button(settings_frame, text="Show Status", command=self.app.show_settings_status)
        self.app.show_status_btn.grid(row=2, column=0, sticky=tk.W, pady=(5, 0))
        
    def _create_progress_frame(self, parent):
        """Create progress frame"""
        progress_frame = ttk.LabelFrame(parent, text="Progress", padding="10")
        progress_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.app.progress_var = tk.DoubleVar()
        self.app.progress_bar = ttk.Progressbar(progress_frame, variable=self.app.progress_var, maximum=100)
        self.app.progress_bar.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 5))
        
        self.app.status_label = ttk.Label(progress_frame, text="Ready to start...")
        self.app.status_label.grid(row=1, column=0, columnspan=3, sticky=tk.W)
        
    def _create_output_frame(self, parent):
        """Create output frame with text widget"""
        output_frame = ttk.LabelFrame(parent, text="Output", padding="10")
        output_frame.grid(row=8, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        self.app.output_text = tk.Text(output_frame, height=10, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(output_frame, orient="vertical", command=self.app.output_text.yview)
        self.app.output_text.configure(yscrollcommand=scrollbar.set)
        
        self.app.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configure grid weights for output frame
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)
        
    def _configure_grid_weights(self, main_frame):
        """Configure grid weights for responsive layout"""
        self.app.root.columnconfigure(0, weight=1)
        self.app.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(8, weight=1)
        
    def open_output_folder(self):
        """Open the output folder where PDFs are saved"""
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        if not os.path.exists(desktop_path):
            desktop_path = os.getcwd()
        
        try:
            # Open folder in Finder (macOS) or File Explorer (Windows)
            system = platform.system()
            if system == "Darwin":  # macOS
                subprocess.run(["open", desktop_path])
            elif system == "Windows":
                subprocess.run(["explorer", desktop_path])
            else:  # Linux
                subprocess.run(["xdg-open", desktop_path])
                
            self.app.log_message(f"Opened output folder: {desktop_path}")
        except Exception as e:
            self.app.log_message(f"Could not open folder: {e}")
            from tkinter import messagebox
            messagebox.showinfo("Output Location", f"PDFs are saved to:\n{desktop_path}")
            
    def save_settings_manually(self):
        """Manually save current settings"""
        if hasattr(self.app, 'settings_manager'):
            if self.app.settings_manager.save_settings():
                self.app.log_message("Settings saved manually")
            else:
                self.app.log_message("Failed to save settings")
        else:
            self.app.log_message("Settings manager not available")
            
    def clear_settings(self):
        """Clear saved settings"""
        if hasattr(self.app, 'settings_manager'):
            if self.app.settings_manager.clear_settings():
                # Reset UI elements
                self.reset_selections()
                self.app.log_message("Settings cleared and UI reset")
            else:
                self.app.log_message("Failed to clear settings")
        else:
            self.app.log_message("Settings manager not available")
            
    def reset_selections(self):
        """Reset current selections without clearing saved settings"""
        # Reset coordinates
        self.app.top_left = None
        self.app.bottom_right = None
        self.app.next_button_pos = None
        
        # Reset UI labels
        self.app.area_status_label.config(text="No area selected", foreground="red")
        self.app.button_status_label.config(text="No button selected", foreground="red")
        
        # Reset page count to default
        self.app.pages_var.set("10")
        
        self.app.log_message("Selections reset - you can now select new area and button positions")
