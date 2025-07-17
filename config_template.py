# Book Scanner Configuration
# Copy this file to config.py and edit the values below

# Google Vision API Credentials
# Download your service account JSON file from Google Cloud Console
# and provide the full path here
GOOGLE_CREDENTIALS_PATH = "/path/to/your/credentials.json"

# Default capture settings
DEFAULT_PAGES = 10
DEFAULT_DELAY = 1.5  # Seconds to wait between page clicks

# Output settings
PDF_OUTPUT_NAME = "captured_book.pdf"
TEXT_OUTPUT_SUFFIX = ".txt"
OUTPUT_FOLDER = "~/Desktop"  # Where to save PDFs (~ means home directory)
USE_TIMESTAMP = True  # Add timestamp to filename to avoid overwriting

# Image preprocessing settings
ENABLE_PREPROCESSING = True
GRAYSCALE_CONVERSION = True

# GUI settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
OVERLAY_ALPHA = 0.3
