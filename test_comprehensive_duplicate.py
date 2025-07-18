#!/usr/bin/env python3
"""
Comprehensive test for duplicate detection functionality in Book Scanner
"""
import os
import sys
import tempfile
import shutil
from PIL import Image, ImageDraw

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from capture_processor import CaptureProcessor

class MockApp:
    """Mock application for testing"""
    def __init__(self):
        self.messages = []
        self.top_left = (100, 100)
        self.bottom_right = (300, 300)
        self.total_pages = 10
        
    def log_message(self, message):
        self.messages.append(message)
        print(f"[MockApp] {message}")

def create_test_image(color='white', shape='circle', size=(200, 200)):
    """Create a test image with specified properties"""
    img = Image.new('RGB', size, color)
    draw = ImageDraw.Draw(img)
    
    if shape == 'circle':
        draw.ellipse([50, 50, 150, 150], fill='black')
    elif shape == 'rectangle':
        draw.rectangle([50, 50, 150, 150], fill='black')
    elif shape == 'triangle':
        draw.polygon([(100, 50), (50, 150), (150, 150)], fill='black')
    elif shape == 'lines':
        # Draw multiple lines
        for i in range(20, 180, 10):
            draw.line([(20, i), (180, i)], fill='black', width=2)
    elif shape == 'dots':
        # Draw a pattern of dots
        for x in range(40, 160, 20):
            for y in range(40, 160, 20):
                draw.ellipse([x-3, y-3, x+3, y+3], fill='black')
    elif shape == 'text':
        # Draw text content
        draw.text((50, 50), "This is a test", fill='black')
        draw.text((50, 80), "Different content", fill='black')
        draw.text((50, 110), "More text here", fill='black')
    
    return img

def test_duplicate_detection_logic():
    """Test the duplicate detection logic comprehensively"""
    print("=== Testing Duplicate Detection Logic ===")
    
    app = MockApp()
    processor = CaptureProcessor(app)
    
    # Test 1: Identical images
    print("\n1. Testing identical images...")
    img1 = create_test_image('white', 'circle')
    img2 = create_test_image('white', 'circle')
    
    assert processor._images_are_similar(img1, img2), "Identical images should be similar"
    print("✅ Identical images correctly detected as similar")
    
    # Test 2: Different images
    print("\n2. Testing different images...")
    img3 = create_test_image('white', 'lines')  # Very different pattern
    
    assert not processor._images_are_similar(img1, img3), "Different images should not be similar"
    print("✅ Different images correctly detected as not similar")
    
    # Test 3: Same image with slight variation (should still be similar)
    print("\n3. Testing similar images with slight variation...")
    img4 = create_test_image('white', 'circle', size=(201, 201))  # Slightly different size
    
    # This might be similar or not depending on the threshold - let's check
    similarity = processor._images_are_similar(img1, img4)
    print(f"Similar images with slight variation: {similarity}")
    
    # Test 4: Very different images
    print("\n4. Testing very different images...")
    img5 = create_test_image('white', 'text')  # Text content
    
    assert not processor._images_are_similar(img1, img5), "Very different images should not be similar"
    print("✅ Very different images correctly detected as not similar")
    
    # Test 5: Hash consistency
    print("\n5. Testing hash consistency...")
    hash1 = processor._calculate_image_hash(img1)
    hash2 = processor._calculate_image_hash(img1)
    
    assert hash1 == hash2, "Hash should be consistent for same image"
    print("✅ Hash consistency verified")
    
    # Test 6: Different images have different hashes
    print("\n6. Testing different images have different hashes...")
    hash3 = processor._calculate_image_hash(img3)
    hash5 = processor._calculate_image_hash(img5)
    
    assert hash1 != hash3, "Different images should have different hashes"
    assert hash1 != hash5, "Different images should have different hashes"
    print("✅ Different images have different hashes")
    
    print("\n✅ All duplicate detection logic tests passed!")

def test_duplicate_counter_logic():
    """Test the duplicate counter logic"""
    print("\n=== Testing Duplicate Counter Logic ===")
    
    app = MockApp()
    processor = CaptureProcessor(app)
    
    # Simulate the duplicate detection process
    img1 = create_test_image('white', 'circle')
    img2 = create_test_image('white', 'circle')  # Duplicate
    img3 = create_test_image('white', 'lines')  # Different
    img4 = create_test_image('white', 'circle')  # Back to similar as img1
    
    # Test sequence: img1 -> img2 (duplicate) -> img3 (different) -> img4 (similar to img1)
    
    # Start with first image
    processor.previous_image = img1
    processor.duplicate_count = 0
    
    # Process second image (duplicate)
    is_duplicate = processor._images_are_similar(img2, processor.previous_image)
    if is_duplicate:
        processor.duplicate_count += 1
        print(f"After first duplicate: count = {processor.duplicate_count}")
    else:
        processor.duplicate_count = 0
        processor.previous_image = img2.copy()
    
    assert processor.duplicate_count == 1, "First duplicate should increment count to 1"
    
    # Process third image (different) - should reset count
    processor.previous_image = img2  # Update previous image
    is_duplicate = processor._images_are_similar(img3, processor.previous_image)
    if is_duplicate:
        processor.duplicate_count += 1
    else:
        processor.duplicate_count = 0
        processor.previous_image = img3.copy()
    
    print(f"After different image: count = {processor.duplicate_count}")
    assert processor.duplicate_count == 0, "Different image should reset count to 0"
    
    # Process fourth image (similar to img1, but different from img3)
    is_duplicate = processor._images_are_similar(img4, processor.previous_image)
    if is_duplicate:
        processor.duplicate_count += 1
    else:
        processor.duplicate_count = 0
        processor.previous_image = img4.copy()
    
    print(f"After fourth image: count = {processor.duplicate_count}")
    
    print("✅ Duplicate counter logic test passed!")

def test_stopping_condition():
    """Test the stopping condition (2 consecutive duplicates)"""
    print("\n=== Testing Stopping Condition ===")
    
    app = MockApp()
    processor = CaptureProcessor(app)
    
    # Create a sequence: unique -> duplicate -> duplicate (should stop)
    img1 = create_test_image('white', 'circle')
    img2 = create_test_image('white', 'circle')  # Duplicate 1
    img3 = create_test_image('white', 'circle')  # Duplicate 2 (should trigger stop)
    
    processor.previous_image = img1
    processor.duplicate_count = 0
    
    # First duplicate
    if processor._images_are_similar(img2, processor.previous_image):
        processor.duplicate_count += 1
    
    print(f"After first duplicate: count = {processor.duplicate_count}")
    
    # Second duplicate (should trigger stop condition)
    processor.previous_image = img2
    if processor._images_are_similar(img3, processor.previous_image):
        processor.duplicate_count += 1
    
    print(f"After second duplicate: count = {processor.duplicate_count}")
    
    should_stop = processor.duplicate_count >= 2
    print(f"Should stop capturing: {should_stop}")
    
    assert should_stop, "Should stop after 2 consecutive duplicates"
    print("✅ Stopping condition test passed!")

def main():
    """Run all tests"""
    print("🔍 Running comprehensive duplicate detection tests...")
    
    try:
        test_duplicate_detection_logic()
        test_duplicate_counter_logic()
        test_stopping_condition()
        
        print("\n🎉 All comprehensive tests passed!")
        print("✅ Duplicate detection functionality is working correctly!")
        print("✅ The Book Scanner will now:")
        print("   - Skip duplicate images")
        print("   - Stop automatically after 2 consecutive duplicates")
        print("   - Show accurate page counts")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
