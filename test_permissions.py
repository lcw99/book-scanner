#!/usr/bin/env python3
"""
Test and fix Google Cloud Storage permissions for async OCR
"""

import os
from google.cloud import storage
from google.cloud import iam

def test_bucket_permissions():
    """Test if we can access and write to the GCS bucket"""
    bucket_name = "book-scanner-ocr-bucket"
    
    print("🔍 Testing Google Cloud Storage Permissions")
    print("=" * 50)
    
    try:
        # Initialize the storage client
        storage_client = storage.Client()
        print("✓ Storage client initialized successfully")
        
        # Try to get the bucket
        try:
            bucket = storage_client.get_bucket(bucket_name)
            print(f"✓ Bucket '{bucket_name}' exists and is accessible")
        except Exception as e:
            print(f"❌ Cannot access bucket '{bucket_name}': {e}")
            return False
        
        # Test write permissions with a small test file
        test_blob_name = "permission_test.txt"
        test_content = "This is a test file to check write permissions."
        
        try:
            blob = bucket.blob(test_blob_name)
            blob.upload_from_string(test_content)
            print("✓ Successfully uploaded test file - WRITE permission confirmed")
            
            # Clean up the test file
            blob.delete()
            print("✓ Successfully deleted test file - DELETE permission confirmed")
            
        except Exception as e:
            print(f"❌ Cannot write to bucket: {e}")
            print("\n🔧 SOLUTION NEEDED:")
            print("Your service account needs 'Storage Object Admin' role.")
            return False
        
        print("\n🎉 All permissions are working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing permissions: {e}")
        return False

def get_service_account_info():
    """Get information about the current service account"""
    try:
        storage_client = storage.Client()
        print(f"\n📋 Service Account Information:")
        print(f"Project ID: {storage_client.project}")
        
        # Try to get service account email from credentials
        if hasattr(storage_client._credentials, 'service_account_email'):
            email = storage_client._credentials.service_account_email
            print(f"Service Account: {email}")
        
        return storage_client.project
        
    except Exception as e:
        print(f"Error getting service account info: {e}")
        return None

def show_permission_fix_guide():
    """Show step-by-step guide to fix permissions"""
    print("\n🛠️  HOW TO FIX PERMISSIONS:")
    print("=" * 50)
    print("1. Go to Google Cloud Console")
    print("2. Navigate to IAM & Admin → IAM")
    print("3. Find your service account:")
    print("   vision-service-api@book-scanner-ocr-466206.iam.gserviceaccount.com")
    print("4. Click the pencil icon (Edit)")
    print("5. Click 'ADD ANOTHER ROLE'")
    print("6. Select 'Storage Object Admin'")
    print("7. Click 'SAVE'")
    print("\nAlternatively:")
    print("1. Go to Cloud Storage → Buckets → book-scanner-ocr-bucket")
    print("2. Click 'PERMISSIONS' tab")
    print("3. Click 'GRANT ACCESS'")
    print("4. Add principal: vision-service-api@book-scanner-ocr-466206.iam.gserviceaccount.com")
    print("5. Role: Storage Object Admin")
    print("6. Click 'SAVE'")

if __name__ == "__main__":
    print("Testing Google Cloud Storage permissions for async OCR...")
    
    # Get service account info
    project_id = get_service_account_info()
    
    # Test permissions
    if test_bucket_permissions():
        print("\n✅ Ready to use async OCR!")
        print("You can now run: python test_async_ocr.py")
    else:
        show_permission_fix_guide()
        print("\n💡 After fixing permissions, run this test again.")
