"""
Capture Processor Module for Book Scanner
Contains screenshot capture and OCR processing functionality
"""
import threading
import os
import tempfile
import time
import datetime
from tkinter import messagebox
import pyautogui
import img2pdf
import platform
import subprocess

# Add src directory to path to import our modules
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))
from google_vision_ocr import process_pdf


class CaptureProcessor:
    """Handles screenshot capture and OCR processing functionality"""
    
    def __init__(self, app_instance):
        self.app = app_instance
        
    def _take_high_quality_screenshot(self, region):
        """Take a high-quality screenshot, using native methods on macOS for better resolution"""
        try:
            if platform.system() == 'Darwin':  # macOS
                # Try using macOS screencapture for higher quality
                x, y, width, height = region
                temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
                temp_file.close()
                
                # Use screencapture with region
                cmd = [
                    'screencapture', 
                    '-x',  # No sound
                    '-R', f'{x},{y},{width},{height}',
                    temp_file.name
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
                
                if result.returncode == 0:
                    # Load the screenshot
                    from PIL import Image
                    screenshot = Image.open(temp_file.name)
                    self.app.log_message(f"High-quality capture: {screenshot.size}")
                    
                    # Clean up temp file
                    os.unlink(temp_file.name)
                    return screenshot
                else:
                    self.app.log_message(f"screencapture failed: {result.stderr}, falling back to pyautogui")
                    
            # Fallback to pyautogui for non-macOS or if screencapture fails
            return pyautogui.screenshot(region=region)
            
        except Exception as e:
            self.app.log_message(f"High-quality capture failed: {e}, using pyautogui")
            return pyautogui.screenshot(region=region)
        
    def start_capture_process(self):
        """Start the capture and OCR process"""
        # Validate inputs
        if not self.app.top_left or not self.app.bottom_right:
            messagebox.showerror("Error", "Please select the capture area first!")
            return
            
        if not self.app.next_button_pos:
            messagebox.showerror("Error", "Please select the next button position first!")
            return
            
        try:
            self.app.total_pages = int(self.app.pages_var.get())
            if self.app.total_pages <= 0:
                raise ValueError()
                
            # Auto-save settings with updated page count
            if hasattr(self.app, 'settings_manager'):
                self.app.settings_manager.save_settings()
                
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number of pages!")
            return
            
        # Disable capture button and enable stop button
        self.app.capture_btn.config(state="disabled")
        self.app.stop_btn.config(state="normal")
        self.app.stop_capture_flag = False
        
        # Start capture in separate thread
        self.app.capture_thread = threading.Thread(target=self.capture_and_process, daemon=True)
        self.app.capture_thread.start()
        
    def stop_capture(self):
        """Stop the capture process"""
        self.app.stop_capture_flag = True
        self.app.log_message("Stopping capture process...")
        
    def capture_and_process(self):
        """Main capture and processing function (runs in separate thread)"""
        try:
            # Step 1: Capture screenshots
            self.app.status_label.config(text="Capturing screenshots...")
            self.app.log_message(f"Starting capture of {self.app.total_pages} pages...")
            
            # Hide the GUI window during capture
            self.app.root.withdraw()
            time.sleep(1)  # Give time for window to hide
            
            # Add initial wait to ensure we're ready to capture the current page
            self.app.log_message("Waiting 3 seconds before starting capture...")
            self.app.log_message("Make sure you're on the FIRST page you want to capture!")
            self.app.log_message("Make sure your book reader application is focused and ready!")
            time.sleep(3)  # Give user time to prepare and ensure we capture current page
            
            # Ensure the target application has focus by clicking on the next button area first
            # This ensures the button area is ready and focused for subsequent clicks
            pyautogui.click(self.app.next_button_pos)
            time.sleep(0.5)  # Brief pause after focus click
            
            images = []
            temp_dir = tempfile.mkdtemp()
            
            for i in range(self.app.total_pages):
                if self.app.stop_capture_flag:
                    break
                    
                # Update progress
                progress = (i / self.app.total_pages) * 50  # First 50% for capture
                self.app.progress_var.set(progress)
                
                page_num = str(i).zfill(len(str(self.app.total_pages)))
                file_name = os.path.join(temp_dir, f'book-page-{page_num}.png')
                images.append(file_name)
                
                # Take screenshot with debug logging
                pic_size = (self.app.bottom_right[0] - self.app.top_left[0], 
                          self.app.bottom_right[1] - self.app.top_left[1])
                region = (self.app.top_left[0], self.app.top_left[1], pic_size[0], pic_size[1])
                
                self.app.log_message(f"Capturing page {i+1}/{self.app.total_pages} - Region: {region}")
                
                screenshot = self._take_high_quality_screenshot(region)
                screenshot.save(file_name)
                
                self.app.log_message(f"Saved page {i+1} to {file_name}")
                
                # Click next button (except for last page)
                if i < self.app.total_pages - 1:
                    self.app.log_message(f"Clicking next button at {self.app.next_button_pos}")
                    
                    # Make a click sound for testing feedback
                    if platform.system() == 'Darwin':  # macOS
                        subprocess.run(['afplay', '/System/Library/Sounds/Pop.aiff'], 
                                     capture_output=True)
                    elif platform.system() == 'Windows':
                        import winsound
                        winsound.MessageBeep(winsound.MB_OK)
                    
                    # Add a small delay before clicking to ensure stability
                    time.sleep(0.3)
                    pyautogui.click(self.app.next_button_pos)
                    
                    # Increased wait time for page to load and become ready
                    # This helps prevent the "first click doesn't work" issue
                    time.sleep(2.5)  # Wait for page to load and stabilize
                    
            # Show GUI window again
            self.app.root.deiconify()
            
            if self.app.stop_capture_flag:
                self.app.log_message("Capture stopped by user.")
                return
                
            # Step 2: Convert to PDF
            pdf_path = self._convert_to_pdf(images)
            
            # Step 3: Ask user if they want to proceed with OCR
            proceed_with_ocr = messagebox.askyesno(
                "OCR Processing", 
                f"PDF created successfully!\n\n"
                f"Location: {pdf_path}\n\n"
                f"Would you like to proceed with OCR text extraction?\n"
                f"(This may take several minutes depending on the number of pages)"
            )
            
            if proceed_with_ocr:
                self._perform_ocr(pdf_path)
            else:
                self.app.log_message("OCR processing skipped by user.")
            
            # Final completion message
            self._show_completion_message(pdf_path, ocr_performed=proceed_with_ocr)
            
        except Exception as e:
            self.app.log_message(f"Error: {str(e)}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            
        finally:
            # Re-enable controls
            self.app.capture_btn.config(state="normal")
            self.app.stop_btn.config(state="disabled")
            self.app.root.deiconify()  # Make sure window is visible
            
    def _convert_to_pdf(self, images):
        """Convert captured images to PDF"""
        self.app.status_label.config(text="Converting to PDF...")
        self.app.log_message("Converting images to PDF...")
        
        # Save PDF to Documents/book-scanner folder
        output_folder = os.path.join(os.path.expanduser("~"), "Documents", "book-scanner")
        
        # Create the folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)
        
        # Generate unique filename with timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_filename = f"captured_book_{timestamp}.pdf"
        pdf_path = os.path.join(output_folder, pdf_filename)
        
        with open(pdf_path, "wb") as f:
            f.write(img2pdf.convert(images))
            
        self.app.log_message(f"PDF saved to: {pdf_path}")
        self.app.log_message(f"You can find your book at: {pdf_path}")
        
        return pdf_path
        
    def _perform_ocr(self, pdf_path):
        """Perform OCR processing on the PDF"""
        self.app.status_label.config(text="Performing OCR...")
        self.app.log_message("Starting OCR processing...")
        
        # Check if Google Vision API credentials are set
        if not os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'):
            self.app.log_message("Warning: Google Vision API credentials not set. Please set GOOGLE_APPLICATION_CREDENTIALS environment variable.")
            messagebox.showwarning("Warning", "Google Vision API credentials not set. OCR will be skipped.")
            return None
        
        try:
            output_folder = os.path.dirname(pdf_path)
            process_pdf(pdf_path, output_folder)
            self.app.log_message("OCR processing completed!")
            
            # Update progress to 100%
            self.app.progress_var.set(100)
            
            return output_folder
            
        except Exception as e:
            self.app.log_message(f"OCR Error: {str(e)}")
            messagebox.showerror("OCR Error", f"Failed to perform OCR: {str(e)}")
            return None
            
    def _show_completion_message(self, pdf_path, ocr_performed=True):
        """Show completion message and summary"""
        self.app.status_label.config(text="Process completed!")
        self.app.log_message("All processing completed successfully!")
        self.app.log_message("=" * 50)
        self.app.log_message(f"📁 PDF saved to: {pdf_path}")
        
        # Check if text file was created (only if OCR was performed)
        if ocr_performed:
            output_folder = os.path.dirname(pdf_path)
            text_file_path = os.path.join(output_folder, os.path.basename(pdf_path) + ".txt")
            if os.path.exists(text_file_path):
                self.app.log_message(f"📄 Text file saved to: {text_file_path}")
        else:
            self.app.log_message("📄 OCR processing was skipped - no text file created")
            
        self.app.log_message("=" * 50)
        
        # Open the output folder
        output_folder = os.path.dirname(pdf_path)
        try:
            if platform.system() == 'Darwin':  # macOS
                subprocess.run(['open', output_folder])
            elif platform.system() == 'Windows':
                subprocess.run(['explorer', output_folder])
            elif platform.system() == 'Linux':
                subprocess.run(['xdg-open', output_folder])
            self.app.log_message(f"Opened output folder: {output_folder}")
        except Exception as e:
            self.app.log_message(f"Could not open output folder: {e}")
        
        # Show completion message
        ocr_status = "with OCR text extraction" if ocr_performed else "without OCR"
        messagebox.showinfo("Process Complete", 
                          f"Book capture completed {ocr_status}!\n\n"
                          f"PDF saved to:\n{pdf_path}\n\n"
                          f"The output folder has been opened for you.")
