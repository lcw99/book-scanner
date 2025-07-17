#!/usr/bin/env python3
"""
Debug script to test and view Google Vision OCR annotation output
Run this script to see annotation data that would normally be hidden in GUI applications.
"""

import os
import sys
import json
from pprint import pprint

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from google_vision_ocr import debug_annotation_structure, detect_text_from_image
    print("✓ Successfully imported OCR functions")
except ImportError as e:
    print(f"✗ Failed to import OCR functions: {e}")
    sys.exit(1)

def test_image_ocr():
    """Test OCR on a simple image to see annotation structure"""
    print("\n=== Testing Image OCR ===")
    
    # Create a simple test image with text
    from PIL import Image, ImageDraw, ImageFont
    import io
    
    # Create a simple image with text
    img = Image.new('RGB', (400, 100), color='white')
    draw = ImageDraw.Draw(img)
    
    try:
        # Try to use a system font
        font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 24)
    except:
        font = ImageFont.load_default()
    
    draw.text((10, 30), "This is a test annotation", fill='black', font=font)
    
    # Convert to bytes
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    image_data = buffer.getvalue()
    
    # Perform OCR
    try:
        result = detect_text_from_image(image_data)
        print(f"Detected text: {result}")
        return True
    except Exception as e:
        print(f"OCR failed: {e}")
        return False

def test_gcs_ocr():
    """Test GCS-based OCR if credentials are available"""
    print("\n=== Testing GCS OCR ===")
    
    # Check if credentials are set
    if not os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'):
        print("GOOGLE_APPLICATION_CREDENTIALS not set. Skipping GCS test.")
        return False
    
    # This would require actual GCS setup, so just show how to call it
    print("To test GCS OCR with annotation debugging:")
    print("debug_info = debug_annotation_structure('gs://bucket/file.pdf', 'gs://bucket/output/')")
    print("pprint(debug_info)")
    return True

def main():
    print("Google Vision OCR Debug Tool")
    print("=" * 40)
    
    # Test basic image OCR
    if test_image_ocr():
        print("✓ Basic OCR test passed")
    else:
        print("✗ Basic OCR test failed")
    
    # Test GCS OCR setup
    test_gcs_ocr()
    
    print("\n=== Annotation Structure Info ===")
    print("When you run OCR, annotations contain:")
    print("- text: The extracted text content")
    print("- pages: Information about document pages")
    print("- paragraphs: Text paragraph information") 
    print("- words: Individual word details with bounding boxes")
    print("- symbols: Character-level information")
    print("\nTo see full annotation output in GUI applications,")
    print("use the debug_annotation_structure() function or")
    print("check the terminal where your GUI was launched.")

if __name__ == "__main__":
    main()
