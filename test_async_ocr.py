#!/usr/bin/env python3
"""
Test script for async document OCR with Google Cloud Storage.
This script tests the async document detection functionality.
"""

import os
import sys
from src.google_vision_ocr import upload_to_gcs_and_process

def test_async_ocr():
    """Test the async OCR functionality with a sample PDF."""
    
    # Configuration
    bucket_name = "book-scanner-ocr-bucket"
    input_folder = "./input_pdfs"
    output_folder = "./output_text"
    
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Check if input folder exists and has PDF files
    if not os.path.exists(input_folder):
        print(f"Error: Input folder '{input_folder}' does not exist.")
        print("Please create the folder and add some PDF files to test.")
        return False
    
    # Find PDF files
    pdf_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print(f"No PDF files found in '{input_folder}'.")
        print("Please add some PDF files to test the async OCR functionality.")
        return False
    
    # Test with the first PDF
    pdf_file = pdf_files[0]
    pdf_path = os.path.join(input_folder, pdf_file)
    
    print(f"Testing async OCR with: {pdf_file}")
    print(f"Using bucket: {bucket_name}")
    print("-" * 50)
    
    try:
        # Process with async document detection
        print("Starting async document detection...")
        extracted_text = upload_to_gcs_and_process(pdf_path, bucket_name)
        
        # Save the result
        output_file = os.path.join(output_folder, f"{pdf_file}_async.txt")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(extracted_text)
        
        print(f"✅ Success! Async processing completed!")
        print(f"📄 Output saved to: {output_file}")
        print(f"📊 Extracted text length: {len(extracted_text)} characters")
        
        # Show first 200 characters as preview
        if extracted_text:
            preview = extracted_text[:200] + "..." if len(extracted_text) > 200 else extracted_text
            print(f"📖 Preview: {preview}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during async processing: {e}")
        print("\nTroubleshooting checklist:")
        print("1. ✓ GCS bucket created: book-scanner-ocr-bucket")
        print("2. ? Cloud Storage API enabled")
        print("3. ? google-cloud-storage package installed")
        print("4. ? GOOGLE_APPLICATION_CREDENTIALS environment variable set")
        print("5. ? Proper permissions for the service account")
        
        print(f"\nTo check your environment:")
        print(f"- Credentials: {os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', 'NOT SET')}")
        
        return False

def check_prerequisites():
    """Check if all prerequisites are met."""
    print("Checking prerequisites...")
    
    # Check if google-cloud-storage is installed
    try:
        from google.cloud import storage
        print("✓ google-cloud-storage package is installed")
    except ImportError:
        print("❌ google-cloud-storage package not installed")
        print("   Run: pip install google-cloud-storage")
        return False
    
    # Check credentials
    creds_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    if creds_path:
        if os.path.exists(creds_path):
            print(f"✓ Credentials file found: {creds_path}")
        else:
            print(f"❌ Credentials file not found: {creds_path}")
            return False
    else:
        print("❌ GOOGLE_APPLICATION_CREDENTIALS environment variable not set")
        return False
    
    # Check if we can create a storage client
    try:
        from google.cloud import storage
        client = storage.Client()
        print("✓ Google Cloud Storage client created successfully")
    except Exception as e:
        print(f"❌ Error creating Storage client: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🔍 Google Vision API Async OCR Test")
    print("=" * 50)
    
    if check_prerequisites():
        print("\n🚀 Starting async OCR test...")
        success = test_async_ocr()
        
        if success:
            print("\n🎉 Test completed successfully!")
        else:
            print("\n💡 Please fix the issues above and try again.")
    else:
        print("\n💡 Please fix the prerequisites and try again.")
