# Book Scanner - Cross Platform Application

A Python GUI application that captures book pages from your screen, converts them to PDF, and extracts text using Google Vision API OCR.

## Features

- **Cross-platform**: Works on Windows and macOS
- **GUI Interface**: Easy-to-use graphical interface for area selection
- **Automated Capture**: Automatically captures multiple pages by clicking next button
- **PDF Conversion**: Converts captured images to PDF format
- **OCR Processing**: Extracts text from images using Google Vision API
- **Progress Tracking**: Real-time progress updates and status messages

## Installation

### Prerequisites

- Python 3.7 or higher
- **Recommended**: Anaconda or Miniconda for better dependency management
- Internet connection for package installation

### Quick Setup with Conda (Recommended)

If you have Anaconda or Miniconda installed:

1. Clone or download this repository
2. Open terminal/command prompt in the project directory
3. Run the setup script (it will automatically detect and use conda):

```bash
# On macOS/Linux:
python3 setup.py

# On Windows:
python setup.py
```

### Alternative: Create Environment Manually

If you prefer to set up the conda environment manually:

```bash
# Create environment from yml file
conda env create -f environment.yml

# Or create manually
conda create -n book-scanner python=3.9
conda activate book-scanner
conda install -c conda-forge pillow numpy opencv poppler
pip install pyautogui img2pdf google-cloud-vision pdf2image
```

### Fallback: Pip Installation

If you don't have conda, the setup script will automatically use pip:

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Install system dependencies:
   - **macOS**: `brew install poppler`
   - **Windows**: poppler is automatically handled
   - **Linux**: `sudo apt-get install poppler-utils` (Ubuntu/Debian)

## Google Vision API Setup

To use OCR functionality, you need to set up Google Vision API:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the Vision API
4. Create a service account and download the JSON key file
5. Set the environment variable:
   - **Windows**: `set GOOGLE_APPLICATION_CREDENTIALS=path\to\your\credentials.json`
   - **macOS/Linux**: `export GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/credentials.json`

Alternatively, edit `src/google_vision_ocr.py` and add the path directly:
```python
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'/path/to/your/credentials.json'
```

## Usage

### Running the Application

The setup script creates launcher scripts that automatically handle the conda environment:

- **Windows**: Double-click `run_book_scanner.bat` or run `python run_book_scanner.py`
- **macOS/Linux**: Run `./run_book_scanner.sh` or `python3 run_book_scanner.py`

### Manual Execution with Conda

If you want to run manually with the conda environment:

```bash
# Activate the environment
conda activate book-scanner

# Run the application
python app/book_scanner_gui.py

# Or use conda run (without activating)
conda run -n book-scanner python app/book_scanner_gui.py
```

### Using the Application

1. **Select Book Page Area**:
   - Click "Select Page Area" button
   - The window will minimize and show a transparent overlay
   - Drag to select the area where book pages appear
   - Release to confirm selection

2. **Select Next Page Button**:
   - Click "Select Next Button" button
   - Click on the location of the "Next Page" button in your book reader

3. **Set Total Pages**:
   - Enter the number of pages you want to capture

4. **Start Capture & OCR**:
   - Click "Start Capture & OCR" to begin the process
   - The app will automatically capture each page and click next
   - After capture, it will convert to PDF and perform OCR

### Output Files

- **PDF**: `captured_book.pdf` - Contains all captured pages
- **Text**: `captured_book.pdf.txt` - OCR extracted text (if Google Vision API is configured)

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure all dependencies are installed with `pip install -r requirements.txt`

2. **Permission Errors on macOS**: 
   - Go to System Preferences > Security & Privacy > Privacy
   - Add Python to "Screen Recording" and "Accessibility"

3. **Google Vision API Errors**:
   - Verify credentials file path is correct
   - Check that Vision API is enabled in Google Cloud Console
   - Ensure billing is set up for your Google Cloud project

4. **Poppler Errors**:
   - **macOS**: Install with `brew install poppler`
   - **Windows**: Should work automatically with pdf2image
   - **Linux**: Install with package manager (`apt-get install poppler-utils`)

### Tips for Best Results

- Use a stable book reader application (web browser, PDF reader, etc.)
- Ensure good contrast between text and background
- Select the area precisely to avoid capturing navigation elements
- Test with a few pages first before capturing an entire book
- Make sure the next page button is consistently in the same location

## File Structure

```
book-scanner/
├── app/
│   └── book_scanner_gui.py     # Main GUI application
├── src/
│   ├── capture_screen.py       # Original capture logic
│   └── google_vision_ocr.py    # OCR processing
├── requirements.txt            # Python dependencies
├── setup.py                   # Setup script
├── run_book_scanner.py        # Application launcher
├── run_book_scanner.bat       # Windows launcher
├── run_book_scanner.sh        # Unix launcher
└── README.md                  # This file
```

## Technical Details

### Dependencies

- **Pillow**: Image processing and manipulation
- **pyautogui**: Screen capture and mouse automation
- **img2pdf**: Converting images to PDF
- **google-cloud-vision**: Google Vision API for OCR
- **pdf2image**: Converting PDF to images
- **opencv-python**: Image preprocessing
- **tkinter**: GUI framework (built into Python)

### Cross-Platform Compatibility

The application is designed to work on both Windows and macOS:
- Uses `tkinter` for GUI (cross-platform)
- Handles different path separators automatically
- Provides platform-specific installation instructions
- Uses appropriate launcher scripts for each platform

## License

This project is open source. Feel free to modify and distribute according to your needs.

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.
