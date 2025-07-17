# Book Scanner - Modular Structure

The Book Scanner application has been refactored into a modular structure for easier maintenance and development.

## File Structure

### `/app/` - Main Application Directory

#### Core Files:
- **`book_scanner_gui.py`** - Main application entry point and coordinator
  - Contains the main `BookScannerApp` class
  - Initializes and coordinates all components
  - Handles delegation to specialized modules
  - ~80 lines (reduced from ~730 lines)

#### Modular Components:

- **`gui_components.py`** - GUI Creation and Layout
  - Handles all tkinter widget creation
  - Manages layout and styling
  - Contains the `GUIComponents` class
  - Responsible for creating all UI elements

- **`selection_handlers.py`** - Area and Button Selection
  - Manages screen area selection functionality
  - Handles overlay creation for selection
  - Contains both normal and alternative selection methods
  - Contains the `SelectionHandlers` class

- **`capture_processor.py`** - Screenshot Capture and OCR
  - Handles the main capture process
  - Manages threading for non-blocking operations
  - Processes PDF conversion and OCR
  - Contains the `CaptureProcessor` class

## Benefits of Modular Structure

1. **Easier Maintenance**: Each component has a single responsibility
2. **Better Organization**: Related functionality is grouped together
3. **Improved Readability**: Smaller, focused files are easier to understand
4. **Enhanced Testability**: Individual components can be tested separately
5. **Simplified Debugging**: Issues can be isolated to specific modules
6. **Future Extensions**: New features can be added as separate modules

## How to Modify Core Logic

### To modify GUI elements:
- Edit `gui_components.py`
- The `GUIComponents` class handles all widget creation and layout

### To modify selection behavior:
- Edit `selection_handlers.py`
- The `SelectionHandlers` class manages both overlay and alternative selection methods

### To modify capture/OCR process:
- Edit `capture_processor.py` 
- The `CaptureProcessor` class handles the main workflow logic

### To modify main application flow:
- Edit `book_scanner_gui.py`
- The main `BookScannerApp` class coordinates between components

## Component Communication

All components receive a reference to the main app instance (`self.app`) which allows them to:
- Access shared state variables (coordinates, settings, etc.)
- Update GUI elements (status labels, progress bars, etc.)
- Call logging methods
- Access other components if needed

This design maintains loose coupling while enabling necessary communication between components.
