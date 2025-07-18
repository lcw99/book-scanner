#!/usr/bin/env python3
"""
Test script for duplicate image detection functionality
"""
import os
import sys
import tempfile
from PIL import Image, ImageDraw

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from capture_processor import CaptureProcessor

class MockApp:
    """Mock application for testing"""
    def __init__(self):
        self.messages = []
        
    def log_message(self, message):
        self.messages.append(message)
        print(f"[TEST] {message}")

def test_duplicate_detection():
    """Test the duplicate detection functionality"""
    print("Testing duplicate image detection...")
    
    # Create mock app
    app = MockApp()
    processor = CaptureProcessor(app)
    
    # Create test images
    # Image 1: White background with black circle
    img1 = Image.new('RGB', (100, 100), 'white')
    draw1 = ImageDraw.Draw(img1)
    draw1.ellipse([25, 25, 75, 75], fill='black')
    
    # Image 2: Same as image 1 (duplicate)
    img2 = Image.new('RGB', (100, 100), 'white')
    draw2 = ImageDraw.Draw(img2)
    draw2.ellipse([25, 25, 75, 75], fill='black')
    
    # Image 3: Different - white background with black rectangle
    img3 = Image.new('RGB', (100, 100), 'white')
    draw3 = ImageDraw.Draw(img3)
    draw3.rectangle([25, 25, 75, 75], fill='black')
    
    # Test hash calculation
    hash1 = processor._calculate_image_hash(img1)
    hash2 = processor._calculate_image_hash(img2)
    hash3 = processor._calculate_image_hash(img3)
    
    print(f"Hash 1: {hash1}")
    print(f"Hash 2: {hash2}")
    print(f"Hash 3: {hash3}")
    
    # Test similarity detection
    similar_1_2 = processor._images_are_similar(img1, img2)
    similar_1_3 = processor._images_are_similar(img1, img3)
    
    print(f"Image 1 and 2 are similar: {similar_1_2}")
    print(f"Image 1 and 3 are similar: {similar_1_3}")
    
    # Test results
    assert similar_1_2 == True, "Identical images should be detected as similar"
    assert similar_1_3 == False, "Different images should not be detected as similar"
    
    print("✅ All duplicate detection tests passed!")

def test_hash_consistency():
    """Test that hash calculation is consistent"""
    print("\nTesting hash consistency...")
    
    app = MockApp()
    processor = CaptureProcessor(app)
    
    # Create the same image multiple times
    img = Image.new('RGB', (100, 100), 'white')
    draw = ImageDraw.Draw(img)
    draw.ellipse([25, 25, 75, 75], fill='black')
    
    # Calculate hash multiple times
    hash1 = processor._calculate_image_hash(img)
    hash2 = processor._calculate_image_hash(img)
    hash3 = processor._calculate_image_hash(img)
    
    assert hash1 == hash2 == hash3, "Hash should be consistent for the same image"
    
    print("✅ Hash consistency test passed!")

if __name__ == "__main__":
    test_duplicate_detection()
    test_hash_consistency()
    print("\n🎉 All tests passed! Duplicate detection is working correctly.")
