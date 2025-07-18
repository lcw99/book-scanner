"""
Settings Manager Module for Book Scanner
Handles saving and loading user preferences and coordinates
"""
import json
import os
from tkinter import messagebox


class SettingsManager:
    """Handles saving and loading application settings"""
    
    def __init__(self, app_instance):
        self.app = app_instance
        self.settings_file = os.path.join(os.path.dirname(__file__), 'book_scanner_settings.json')
        
    def save_settings(self):
        """Save current settings to file"""
        settings = {
            'top_left': self.app.top_left,
            'bottom_right': self.app.bottom_right,
            'next_button_pos': self.app.next_button_pos,
            'total_pages': self.app.pages_var.get() if hasattr(self.app, 'pages_var') else "10",
            'base_location': self.app.base_location_var.get() if hasattr(self.app, 'base_location_var') and self.app.base_location_var else "",
            'base_filename': self.app.base_filename_var.get() if hasattr(self.app, 'base_filename_var') and self.app.base_filename_var else "",
            'version': '1.0'
        }
        
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f, indent=2)
            self.app.log_message(f"Settings saved to {self.settings_file}")
            return True
        except Exception as e:
            self.app.log_message(f"Failed to save settings: {e}")
            return False
            
    def load_settings(self):
        """Load settings from file"""
        if not os.path.exists(self.settings_file):
            self.app.log_message("No previous settings found")
            return False
            
        try:
            with open(self.settings_file, 'r') as f:
                settings = json.load(f)
                
            # Restore coordinates
            if settings.get('top_left') and settings.get('bottom_right'):
                self.app.top_left = tuple(settings['top_left'])
                self.app.bottom_right = tuple(settings['bottom_right'])
                self.app.area_status_label.config(
                    text=f"Area: {self.app.top_left} to {self.app.bottom_right}", 
                    foreground="green"
                )
                self.app.log_message(f"Restored capture area: {self.app.top_left} to {self.app.bottom_right}")
                
            if settings.get('next_button_pos'):
                self.app.next_button_pos = tuple(settings['next_button_pos'])
                self.app.button_status_label.config(
                    text=f"Button at: {self.app.next_button_pos}", 
                    foreground="green"
                )
                self.app.log_message(f"Restored next button position: {self.app.next_button_pos}")
                
            # Restore page count
            if settings.get('total_pages'):
                self.app.pages_var.set(settings['total_pages'])
                
            # Restore base location
            if settings.get('base_location') and hasattr(self.app, 'base_location_var') and self.app.base_location_var:
                self.app.base_location_var.set(settings['base_location'])
                self.app.log_message(f"Restored base location: {settings['base_location']}")
                
            # Restore base filename  
            if settings.get('base_filename') and hasattr(self.app, 'base_filename_var') and self.app.base_filename_var:
                self.app.base_filename_var.set(settings['base_filename'])
                self.app.log_message(f"Restored base filename: {settings['base_filename']}")
            
            # For backward compatibility with old settings files
            elif settings.get('base_filename') and hasattr(self.app, 'base_filename_var') and self.app.base_filename_var:
                # Try to split old combined path into location and filename
                old_path = settings['base_filename']
                if os.path.dirname(old_path) and os.path.basename(old_path):
                    if hasattr(self.app, 'base_location_var') and self.app.base_location_var:
                        self.app.base_location_var.set(os.path.dirname(old_path))
                    self.app.base_filename_var.set(os.path.basename(old_path))
                    self.app.log_message(f"Migrated old settings - Location: {os.path.dirname(old_path)}, Filename: {os.path.basename(old_path)}")
                else:
                    self.app.base_filename_var.set(old_path)
                    self.app.log_message(f"Restored legacy filename: {old_path}")
                
            self.app.log_message("Previous settings restored successfully!")
            return True
            
        except Exception as e:
            self.app.log_message(f"Failed to load settings: {e}")
            return False
            
    def auto_save_on_selection(self):
        """Automatically save settings when area or button is selected"""
        if self.app.top_left and self.app.bottom_right and self.app.next_button_pos:
            self.save_settings()
            
    def clear_settings(self):
        """Clear saved settings"""
        try:
            if os.path.exists(self.settings_file):
                os.remove(self.settings_file)
                self.app.log_message("Settings cleared")
                return True
        except Exception as e:
            self.app.log_message(f"Failed to clear settings: {e}")
        return False
        
    def export_settings(self, export_path):
        """Export settings to a specific path"""
        try:
            if os.path.exists(self.settings_file):
                import shutil
                shutil.copy2(self.settings_file, export_path)
                self.app.log_message(f"Settings exported to {export_path}")
                return True
        except Exception as e:
            self.app.log_message(f"Failed to export settings: {e}")
        return False
        
    def import_settings(self, import_path):
        """Import settings from a specific path"""
        try:
            if os.path.exists(import_path):
                import shutil
                shutil.copy2(import_path, self.settings_file)
                self.load_settings()
                self.app.log_message(f"Settings imported from {import_path}")
                return True
        except Exception as e:
            self.app.log_message(f"Failed to import settings: {e}")
        return False
