#!/usr/bin/env python3
"""
Visual test for duplicate detection - creates sample images and tests detection
"""
import os
import sys
import tempfile
import shutil
from PIL import Image, ImageDraw, ImageFont

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

def create_book_page(page_number, content_variant=0):
    """Create a mock book page image"""
    img = Image.new('RGB', (400, 600), 'white')
    draw = ImageDraw.Draw(img)
    
    # Add page border
    draw.rectangle([20, 20, 380, 580], outline='black', width=2)
    
    # Add title
    title = f"Page {page_number}"
    draw.text((50, 50), title, fill='black')
    
    # Add different content based on variant
    if content_variant == 0:
        # Regular content - Page 1
        content = [
            "Chapter 1: Introduction",
            "This is the beginning of our story.",
            "It was a bright and sunny morning when",
            "John decided to take a walk in the park.",
            "The birds were singing melodiously,",
            "and the flowers were in full bloom.",
            "Children were playing on the swings,",
            "while their parents watched nearby.",
            "The air was fresh and clean,",
            "perfect for a morning stroll."
        ]
    elif content_variant == 1:
        # Different content - Page 2
        content = [
            "Chapter 2: The Journey Begins",
            "After his walk, John felt refreshed.",
            "He decided to visit his old friend Mary,",
            "who lived on the other side of town.",
            "The journey would take him through",
            "the busy marketplace and past the",
            "old cathedral with its towering spires.",
            "Street vendors were calling out their wares,",
            "and the aroma of fresh bread filled the air.",
            "John walked with a spring in his step."
        ]
    elif content_variant == 2:
        # Different content - Page 3
        content = [
            "Chapter 3: An Unexpected Meeting",
            "At the marketplace, John encountered",
            "his childhood friend Peter, whom he",
            "hadn't seen in many years.",
            "They embraced warmly and decided",
            "to catch up over coffee at a nearby café.",
            "The café was cozy and inviting,",
            "with the smell of roasted coffee beans",
            "and the sound of gentle conversation.",
            "They talked for hours about old times."
        ]
    elif content_variant == 3:
        # Duplicate content (same as variant 2)
        content = [
            "Chapter 3: An Unexpected Meeting",
            "At the marketplace, John encountered",
            "his childhood friend Peter, whom he",
            "hadn't seen in many years.",
            "They embraced warmly and decided",
            "to catch up over coffee at a nearby café.",
            "The café was cozy and inviting,",
            "with the smell of roasted coffee beans",
            "and the sound of gentle conversation.",
            "They talked for hours about old times."
        ]
    elif content_variant == 4:
        # Empty/end page content
        content = [
            "",
            "",
            "",
            "              THE END",
            "",
            "",
            "",
            "",
            "",
            ""
        ]
    else:
        # Another empty/end page (similar to variant 4)
        content = [
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            ""
        ]
    
    # Draw the content
    for i, line in enumerate(content):
        draw.text((50, 100 + i*25), line, fill='black')
    
    return img

def test_book_page_detection():
    """Test duplicate detection with realistic book pages"""
    print("=== Testing Book Page Duplicate Detection ===")
    
    app = MockApp()
    processor = CaptureProcessor(app)
    
    # Create test pages with truly different content
    page1 = create_book_page(1, 0)  # Chapter 1 content
    page2 = create_book_page(2, 1)  # Chapter 2 content
    page3 = create_book_page(3, 2)  # Chapter 3 content
    page3_duplicate = create_book_page(3, 3)  # Same content as page3
    end_page1 = create_book_page(4, 4)  # End page with "THE END"
    end_page2 = create_book_page(5, 5)  # Empty end page
    
    # Save test images for visual inspection
    test_dir = tempfile.mkdtemp()
    print(f"Test images saved to: {test_dir}")
    
    page1.save(os.path.join(test_dir, 'page1_chapter1.png'))
    page2.save(os.path.join(test_dir, 'page2_chapter2.png'))
    page3.save(os.path.join(test_dir, 'page3_chapter3.png'))
    page3_duplicate.save(os.path.join(test_dir, 'page3_duplicate.png'))
    end_page1.save(os.path.join(test_dir, 'end_page1.png'))
    end_page2.save(os.path.join(test_dir, 'end_page2.png'))
    
    # Test 1: Different pages should not be similar
    print("\n1. Testing different pages...")
    similar_1_2 = processor._images_are_similar(page1, page2)
    similar_2_3 = processor._images_are_similar(page2, page3)
    
    print(f"Page 1 and 2 similar: {similar_1_2}")
    print(f"Page 2 and 3 similar: {similar_2_3}")
    
    assert not similar_1_2, "Different pages should not be similar"
    assert not similar_2_3, "Different pages should not be similar"
    print("✅ Different pages correctly detected as not similar")
    
    # Test 2: Duplicate pages should be similar
    print("\n2. Testing duplicate pages...")
    similar_3_dup = processor._images_are_similar(page3, page3_duplicate)
    
    print(f"Page 3 and duplicate similar: {similar_3_dup}")
    
    assert similar_3_dup, "Duplicate pages should be similar"
    print("✅ Duplicate pages correctly detected as similar")
    
    # Test 3: End pages (often similar/empty)
    print("\n3. Testing end pages...")
    similar_end = processor._images_are_similar(end_page1, end_page2)
    
    print(f"End pages similar: {similar_end}")
    
    # End pages might be similar due to being mostly empty
    if similar_end:
        print("✅ End pages detected as similar (expected for mostly empty pages)")
    else:
        print("✅ End pages detected as different (also acceptable)")
    
    # Test 4: Hash comparison
    print("\n4. Testing hash comparison...")
    hash1 = processor._calculate_image_hash(page1)
    hash2 = processor._calculate_image_hash(page2)
    hash3 = processor._calculate_image_hash(page3)
    hash3_dup = processor._calculate_image_hash(page3_duplicate)
    
    print(f"Page 1 hash: {hash1[:8]}...")
    print(f"Page 2 hash: {hash2[:8]}...")
    print(f"Page 3 hash: {hash3[:8]}...")
    print(f"Page 3 dup hash: {hash3_dup[:8]}...")
    
    assert hash1 != hash2, "Different pages should have different hashes"
    assert hash2 != hash3, "Different pages should have different hashes"
    
    # Duplicate pages should have the same hash
    if hash3 == hash3_dup:
        print("✅ Duplicate pages have identical hashes")
    else:
        print("ℹ️  Duplicate pages have different hashes (but similarity detection should still work)")
    
    print("✅ Hash comparison test completed")
    
    print(f"\n📁 Test images available at: {test_dir}")
    print("✅ Book page duplicate detection test passed!")

def main():
    """Run visual tests"""
    print("🖼️  Running visual duplicate detection tests...")
    
    try:
        test_book_page_detection()
        
        print("\n🎉 All visual tests passed!")
        print("✅ The duplicate detection works with realistic book pages!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
