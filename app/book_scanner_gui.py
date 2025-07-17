import tkinter as tk
from tkinter import messagebox
import threading
import pyautogui
import os
import sys

# Add current directory to Python path to find our modules
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import our modular components
from gui_components import GUIComponents
from selection_handlers import SelectionHandlers
from capture_processor import CaptureProcessor
from settings_manager import SettingsManager

class BookScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Scanner - Cross Platform")
        
        # Set window to full screen height and reasonable width
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"1200x{screen_height - 100}")  # Full height minus some margin for dock/taskbar
        
        # Variables for screen coordinates
        self.top_left = None
        self.bottom_right = None
        self.next_button_pos = None
        self.total_pages = 0
        self.capture_area = None
        self.selecting_area = False
        self.selecting_button = False
        
        # Control variables
        self.capture_thread = None
        self.stop_capture_flag = False
        
        # Initialize modular components
        self.gui_components = GUIComponents(self)
        self.selection_handlers = SelectionHandlers(self)
        self.capture_processor = CaptureProcessor(self)
        self.settings_manager = SettingsManager(self)
        
        # Create the GUI
        self.gui_components.create_widgets()
        
        # Load previous settings after GUI is created
        self.settings_manager.load_settings()
        
        # Welcome message
        self.log_message("=== Book Scanner Started ===")
        self.log_message("Previous area and button selections are automatically restored if available.")
        self.log_message("Your selections will be automatically saved for next time.")
        self.log_message("Use the Settings section to manage saved preferences.")
        self.log_message("")
        
        # Disable failsafe to prevent interruption during automation
        pyautogui.FAILSAFE = False
        
    def log_message(self, message):
        """Add message to output text widget"""
        # Check if output_text widget exists (GUI has been created)
        if hasattr(self, 'output_text') and self.output_text:
            self.output_text.insert(tk.END, f"{message}\n")
            self.output_text.see(tk.END)
            self.root.update_idletasks()
        else:
            # If GUI not ready, just print to console
            print(f"[Book Scanner] {message}")
        
    # Delegate methods to modular components
    def select_capture_area(self):
        """Delegate to selection handlers - overlay method"""
        self.selection_handlers.select_capture_area()
        
    def select_next_button(self):
        """Delegate to selection handlers"""
        self.selection_handlers.select_next_button()
        
    def start_capture_process(self):
        """Delegate to capture processor"""
        self.capture_processor.start_capture_process()
        
    def stop_capture(self):
        """Delegate to capture processor"""
        self.capture_processor.stop_capture()
        
    def test_capture_area(self):
        """Test capture with selected area to verify coordinates"""
        if not self.top_left or not self.bottom_right:
            self.log_message("Please select capture area first!")
            return
            
        try:
            # Calculate region - with direct approach
            x1, y1 = self.top_left
            x2, y2 = self.bottom_right
            width = x2 - x1
            height = y2 - y1
            
            # Create region tuple in pyautogui format (left, top, width, height)
            region = (x1, y1, width, height)
            
            self.log_message(f"=== Test Capture Debug Info ===")
            self.log_message(f"Stored coordinates - Top-left: {self.top_left}, Bottom-right: {self.bottom_right}")
            self.log_message(f"Calculated region for pyautogui: {region}")
            self.log_message(f"Size: {width}x{height}")
            
            # Add platform info
            import platform
            self.log_message(f"Platform: {platform.system()}")
            
            self.log_message("Hiding main window for test capture...")
            # Hide window for test
            self.root.withdraw()
            import time
            time.sleep(1)  # Give time for window to hide completely
            
            # Take test screenshot
            screenshot = self.capture_processor._take_high_quality_screenshot(region)
            
            # Save to desktop for inspection
            import os
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            test_file = os.path.join(desktop_path, "test_capture.png")
            screenshot.save(test_file)
            
            # Show the captured image in a new window
            self.show_test_capture(screenshot)
            
            # Show window again
            self.root.deiconify()
            self.log_message("Main window restored after test capture")
            
            # Let the user know where the file was saved
            self.log_message(f"✅ Test capture saved to Desktop as 'test_capture.png'")
            messagebox.showinfo("Test Capture Complete", f"Test screenshot saved to your Desktop as 'test_capture.png'.\nCheck if the capture area looks correct.")
            
            self.log_message(f"Test capture saved to: {test_file}")
            self.log_message(f"Captured image size: {screenshot.size}")
            self.log_message("Check the test capture image to verify if coordinates are correct")
            self.log_message("=== End Debug Info ===")
            
        except Exception as e:
            self.root.deiconify()
            self.log_message("Main window restored after test capture error")
            self.log_message(f"Test capture failed: {e}")
            
    def show_settings_status(self):
        """Show current settings status"""
        self.log_message("=== Current Settings Status ===")
        if self.top_left and self.bottom_right:
            self.log_message(f"✓ Capture area: {self.top_left} to {self.bottom_right}")
        else:
            self.log_message("✗ No capture area selected")
            
        if self.next_button_pos:
            self.log_message(f"✓ Next button position: {self.next_button_pos}")
        else:
            self.log_message("✗ No next button position selected")
            
        self.log_message(f"📄 Page count: {self.pages_var.get()}")
        
        # Check if settings file exists
        import os
        settings_file = os.path.join(os.path.dirname(__file__), 'book_scanner_settings.json')
        if os.path.exists(settings_file):
            self.log_message("💾 Settings file exists and will be loaded on startup")
        else:
            self.log_message("💾 No saved settings file found")
        self.log_message("===============================")
        
    def process_existing_pdf(self):
        """Process an existing PDF file with OCR using async Google Vision API"""
        from tkinter import filedialog
        import sys
        import os
        
        # Add src directory to path to import google_vision_ocr
        src_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src')
        if src_dir not in sys.path:
            sys.path.insert(0, src_dir)
        
        try:
            from google_vision_ocr import process_pdf, upload_to_gcs_and_process
        except ImportError as e:
            self.log_message(f"Error importing OCR module: {e}")
            messagebox.showerror("Import Error", "Could not import OCR module. Please check installation.")
            return
        
        # Check if Google Vision API credentials are set
        if not os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'):
            self.log_message("Warning: Google Vision API credentials not set.")
            messagebox.showwarning("Warning", 
                "Google Vision API credentials not set.\n\n"
                "Please set GOOGLE_APPLICATION_CREDENTIALS environment variable\n"
                "or edit src/google_vision_ocr.py to add the credentials path directly.")
            return
        
        # Ask user to choose OCR method
        choice = messagebox.askyesnocancel(
            "Choose OCR Method",
            "Choose OCR processing method:\n\n"
            "• YES: Async Document Detection (Faster, requires Google Cloud Storage)\n"
            "• NO: Traditional Method (Slower, no cloud storage needed)\n"
            "• CANCEL: Cancel operation"
        )
        
        if choice is None:  # User cancelled
            return
        
        use_async = choice  # True for async, False for traditional
        
        # Open file dialog to select PDF
        pdf_file = filedialog.askopenfilename(
            title="Select PDF file for OCR",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        if not pdf_file:
            return  # User cancelled
        
        self.log_message(f"Selected PDF: {os.path.basename(pdf_file)}")
        self.log_message(f"Using {'Async Document Detection' if use_async else 'Traditional'} method")
        
        # Choose output folder
        output_folder = filedialog.askdirectory(
            title="Select output folder for text file",
            initialdir=os.path.dirname(pdf_file)
        )
        
        if not output_folder:
            # Use same folder as PDF if user cancels
            output_folder = os.path.dirname(pdf_file)
        
        self.log_message(f"Output folder: {output_folder}")
        
        # Start OCR processing in a separate thread
        def run_pdf_ocr():
            try:
                if use_async:
                    # Use async document detection with GCS
                    bucket_name = "book-scanner-ocr-bucket"
                    
                    self.status_label.config(text="Processing PDF with Async Document Detection...")
                    self.log_message("Starting Async Document Detection OCR...")
                    self.log_message(f"Using GCS bucket: {bucket_name}")
                    
                    # Process with async method
                    extracted_text = upload_to_gcs_and_process(pdf_file, bucket_name, output_folder=output_folder)
                    
                    # Save the result
                    output_file = os.path.join(output_folder, f"{os.path.basename(pdf_file)}_async.txt")
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(extracted_text)
                    
                    self.status_label.config(text="Async OCR processing completed!")
                    self.log_message("✅ Async OCR processing completed!")
                    self.log_message(f"Text extracted to: {output_file}")
                    self.log_message(f"Extracted {len(extracted_text)} characters")
                    
                else:
                    # Use traditional method
                    self.status_label.config(text="Processing PDF with Traditional OCR...")
                    self.log_message("Starting Traditional OCR processing...")
                    
                    # Process the PDF with traditional method
                    process_pdf(pdf_file, output_folder)
                    
                    # Create output file path for display
                    output_file = os.path.join(output_folder, f"{os.path.basename(pdf_file)}.txt")
                    
                    self.status_label.config(text="Traditional OCR processing completed!")
                    self.log_message("✅ Traditional OCR processing completed!")
                    self.log_message(f"Text extracted to: {output_file}")
                
                # Show completion message
                method_name = "Async Document Detection" if use_async else "Traditional"
                messagebox.showinfo("OCR Complete", 
                    f"{method_name} OCR processing completed!\n\n"
                    f"Text file saved as:\n{os.path.basename(output_file)}\n\n"
                    f"Location: {output_folder}")
                
            except Exception as e:
                error_msg = f"❌ {('Async' if use_async else 'Traditional')} OCR Error: {str(e)}"
                self.status_label.config(text="OCR processing failed")
                self.log_message(error_msg)
                
                if use_async and ("bucket" in str(e).lower() or "storage" in str(e).lower()):
                    messagebox.showerror("Async OCR Error", 
                        f"Failed to process PDF with Async method:\n{str(e)}\n\n"
                        "Troubleshooting:\n"
                        "1. Check if GCS bucket 'book-scanner-ocr-bucket' exists\n"
                        "2. Verify Cloud Storage API is enabled\n"
                        "3. Ensure google-cloud-storage package is installed\n"
                        "4. Check service account permissions\n\n"
                        "Try the Traditional method if Async continues to fail.")
                else:
                    messagebox.showerror("OCR Error", f"Failed to process PDF:\n{str(e)}")
        
        # Run in separate thread to avoid blocking UI
        thread = threading.Thread(target=run_pdf_ocr)
        thread.daemon = True
        thread.start()

    def show_test_capture(self, screenshot):
        """Display the test capture in a new window"""
        from PIL import ImageTk
        
        # Create a new window
        capture_window = tk.Toplevel(self.root)
        capture_window.title("Test Capture Result")
        
        # Get image dimensions
        img_width, img_height = screenshot.size
        
        # Set window size with some padding
        window_width = min(img_width + 40, 1200)
        window_height = min(img_height + 100, 800)
        capture_window.geometry(f"{window_width}x{window_height}")
        
        # Create a header
        header_frame = tk.Frame(capture_window, bg='#e0e0e0')
        header_frame.pack(fill=tk.X, pady=10)
        
        header_label = tk.Label(header_frame, 
                              text="TEST CAPTURE RESULT", 
                              font=('Arial', 14, 'bold'),
                              bg='#e0e0e0')
        header_label.pack(pady=5)
        
        # Create scrollable frame for image
        main_frame = tk.Frame(capture_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add scrollbars if needed
        h_scrollbar = tk.Scrollbar(main_frame, orient=tk.HORIZONTAL)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        v_scrollbar = tk.Scrollbar(main_frame)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create canvas for the image with scrollbars
        canvas = tk.Canvas(main_frame, 
                         width=min(img_width, window_width-40),
                         height=min(img_height, window_height-140),
                         xscrollcommand=h_scrollbar.set, 
                         yscrollcommand=v_scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configure scrollbars
        h_scrollbar.config(command=canvas.xview)
        v_scrollbar.config(command=canvas.yview)
        
        # Convert PIL image to Tkinter PhotoImage
        photo = ImageTk.PhotoImage(screenshot)
        
        # Add image to canvas
        canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        canvas.config(scrollregion=(0, 0, img_width, img_height))
        
        # Create button to close window
        close_btn = tk.Button(capture_window, text="Close", 
                            command=capture_window.destroy,
                            font=('Arial', 12),
                            padx=20, pady=5)
        close_btn.pack(pady=10)
        
        # Keep a reference to the image to prevent garbage collection
        canvas.image = photo

def main():
    root = tk.Tk()
    app = BookScannerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
