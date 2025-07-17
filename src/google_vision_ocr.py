import os
import io
import json
import re
import numpy as np
from PIL import Image
import cv2
from google.cloud import vision
from google.cloud import storage
from pdf2image import convert_from_path
from concurrent.futures import ThreadPoolExecutor, as_completed

# Set the environment variable for Google Vision API credentials
# Option 1: Set the environment variable directly (recommended)
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'/path/to/your/credentials.json'

# Option 2: Set environment variable in your shell before running:
# export GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/credentials.json  (macOS/Linux)
# set GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\your\credentials.json   (Windows)

# The credentials will be automatically detected if the environment variable is set 

def detect_text_from_image(image_data):
    """
    Detects text in an image file using Google Vision API and returns it.
    
    Args:
        image_data (bytes): The image data in bytes format.
        
    Returns:
        str: The detected text.
    """
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_data)

    # Perform text detection
    response = client.text_detection(image=image)
    texts = response.text_annotations

    # Extract and return the detected text (first annotation contains full text)
    if texts:
        return texts[0].description
    else:
        return ""

def async_detect_document(gcs_source_uri, gcs_destination_uri, debug_annotations=False, debug_output_dir=None):
    """
    OCR with PDF/TIFF as source files on GCS using async document text detection.
    This method is more efficient for processing large PDFs.
    
    Args:
        gcs_source_uri (str): GCS URI of the source PDF/TIFF file (e.g., 'gs://bucket/file.pdf')
        gcs_destination_uri (str): GCS URI prefix for output files (e.g., 'gs://bucket/output/')
        debug_annotations (bool): If True, returns both text and annotation data
        debug_output_dir (str, optional): Directory to save debug files. If None, uses current directory.
        
    Returns:
        str or tuple: The full text extracted from the document, or (text, annotations) if debug_annotations=True
    """
    # Supported mime_types are: 'application/pdf' and 'image/tiff'
    mime_type = "application/pdf"

    # How many pages should be grouped into each json output file.
    batch_size = 2

    client = vision.ImageAnnotatorClient()

    feature = vision.Feature(type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)

    gcs_source = vision.GcsSource(uri=gcs_source_uri)
    input_config = vision.InputConfig(gcs_source=gcs_source, mime_type=mime_type)

    gcs_destination = vision.GcsDestination(uri=gcs_destination_uri)
    output_config = vision.OutputConfig(
        gcs_destination=gcs_destination, batch_size=batch_size
    )

    async_request = vision.AsyncAnnotateFileRequest(
        features=[feature], input_config=input_config, output_config=output_config
    )

    operation = client.async_batch_annotate_files(requests=[async_request])

    print("Waiting for the operation to finish.")
    operation.result(timeout=420)

    # Once the request has completed and the output has been
    # written to GCS, we can list all the output files.
    storage_client = storage.Client()

    match = re.match(r"gs://([^/]+)/(.+)", gcs_destination_uri)
    bucket_name = match.group(1)
    prefix = match.group(2)

    bucket = storage_client.get_bucket(bucket_name)

    # List objects with the given prefix, filtering out folders.
    blob_list = [
        blob
        for blob in list(bucket.list_blobs(prefix=prefix))
        if not blob.name.endswith("/")
    ]
    print("Output files:")
    for blob in blob_list:
        print(blob.name)

    # Process all output files and combine the text
    full_text = ""
    annotations_data = []
    for output_blob in blob_list:
        json_string = output_blob.download_as_bytes().decode("utf-8")
        response = json.loads(json_string)

        # Process each page response in the batch
        for page_response in response["responses"]:
            if "fullTextAnnotation" in page_response:
                annotation = page_response["fullTextAnnotation"]
                print(f"Annotation content: {annotation}")
                
                # Also write annotation to a debug file
                import datetime
                import os
                # Use the specified output directory or current directory
                debug_dir = debug_output_dir if debug_output_dir else os.getcwd()
                os.makedirs(debug_dir, exist_ok=True)
                debug_file = os.path.join(debug_dir, f"annotation_debug_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
                # with open(debug_file, 'w', encoding='utf-8') as f:
                #     json.dump(annotation, f, indent=2, ensure_ascii=False)
                # print(f"Annotation data written to: {debug_file}")
                
                annotations_data.append(annotation)
                full_text += annotation["text"] + "\n"

    if debug_annotations:
        return full_text, annotations_data
    return full_text

def upload_to_gcs_and_process(local_pdf_path, bucket_name, source_blob_name=None, destination_prefix=None, debug_annotations=True, output_folder=None):
    """
    Uploads a local PDF to GCS and processes it using async document text detection.
    
    Args:
        local_pdf_path (str): Path to the local PDF file
        bucket_name (str): Name of the GCS bucket
        source_blob_name (str, optional): Name for the uploaded file in GCS. 
                                         If None, uses the original filename.
        destination_prefix (str, optional): Prefix for output files in GCS.
                                           If None, uses 'ocr_output/'.
        debug_annotations (bool): If True, saves annotation data to debug files
        output_folder (str, optional): Folder to save debug files. If None, uses directory of PDF file.
    
    Returns:
        str: The extracted text from the PDF
    """
    if source_blob_name is None:
        source_blob_name = os.path.basename(local_pdf_path)
    
    if destination_prefix is None:
        destination_prefix = "ocr_output/"
    
    # Upload file to GCS
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    
    print(f"Uploading {local_pdf_path} to gs://{bucket_name}/{source_blob_name}")
    blob.upload_from_filename(local_pdf_path)
    
    # Construct URIs
    gcs_source_uri = f"gs://{bucket_name}/{source_blob_name}"
    gcs_destination_uri = f"gs://{bucket_name}/{destination_prefix}"
    
    # Process with async document detection
    if debug_annotations:
        # Use the output folder for debug files, or PDF's directory as fallback
        debug_dir = output_folder if output_folder else os.path.dirname(local_pdf_path)
        extracted_text, annotations = async_detect_document(gcs_source_uri, gcs_destination_uri, debug_annotations=True, debug_output_dir=debug_dir)
        
        # Save annotations to a debug file
        import datetime
        debug_file = os.path.join(debug_dir, f"gui_annotations_debug_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(debug_file, 'w', encoding='utf-8') as f:
            json.dump({
                "source_file": local_pdf_path,
                "total_pages": len(annotations),
                "annotations": annotations
            }, f, indent=2, ensure_ascii=False)
        print(f"GUI Debug: Annotation data saved to {debug_file}")
    else:
        extracted_text = async_detect_document(gcs_source_uri, gcs_destination_uri)
    
    # Clean up: delete the uploaded source file (optional)
    print(f"Cleaning up: deleting gs://{bucket_name}/{source_blob_name}")
    blob.delete()
    
    return extracted_text

def preprocess_image(image):
    """
    Preprocesses the image to enhance OCR accuracy by converting it to grayscale.
    
    Args:
        image (PIL.Image.Image): The image to preprocess.
        
    Returns:
        PIL.Image.Image: The preprocessed image.
    """
    # Convert PIL image to OpenCV format
    image_np = np.array(image)
    gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
    
    # Convert back to PIL image
    return Image.fromarray(gray)

def process_page(page, page_number):
    """
    Processes a single page of PDF: converts to image, preprocesses, performs OCR, and returns the extracted text.
    
    Args:
        page (PIL.Image.Image): The PDF page as a PIL image.
        page_number (int): The page number.
        
    Returns:
        tuple: A tuple containing the page number and extracted text.
    """
    # Convert page to a BytesIO object
    buffer = io.BytesIO()
    page = preprocess_image(page)
    page.save(buffer, format="PNG")
    image_data = buffer.getvalue()

    # Perform OCR on the image data
    extracted_text = detect_text_from_image(image_data)
    
    return (page_number, extracted_text)

def process_pdf(pdf_path, output_folder):
    """
    Processes each page in a PDF file and performs OCR.
    
    Args:
        pdf_path (str): The path to the PDF file.
        output_folder (str): The folder where the output text file will be saved.
    """
    # Convert PDF to images
    pages = convert_from_path(pdf_path)

    # Define the output text file path
    output_text_file = os.path.join(output_folder, f"{os.path.basename(pdf_path)}.txt")
    
    with open(output_text_file, 'w', encoding='utf-8') as text_file:
        # Use ThreadPoolExecutor to process pages in parallel
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(process_page, page, page_number)
                       for page_number, page in enumerate(pages, start=1)]
            results = sorted([future.result() for future in as_completed(futures)], key=lambda x: x[0])
        
        # Write results to file in the correct order
        for page_number, text in results:
            # text_file.write(f"\n--- Page {page_number} ---\n")
            text_file.write(text)
            # text_file.write("\n\n")

def process_all_pdfs(input_folder, output_folder):
    """
    Processes all PDFs in the input folder and stores the results in the output folder.
    
    Args:
        input_folder (str): The folder containing PDF files.
        output_folder (str): The folder where the output text files will be saved.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file_name in os.listdir(input_folder):
        if file_name.endswith(".pdf"):
            pdf_path = os.path.join(input_folder, file_name)
            print(f"Processing {pdf_path}...")
            process_pdf(pdf_path, output_folder)

def debug_annotation_structure(gcs_source_uri, gcs_destination_uri, debug_output_dir=None):
    """
    Debug function to examine the structure of annotations returned by Google Vision API.
    This function can be called from the GUI to see annotation details.
    
    Args:
        gcs_source_uri (str): GCS URI of the source PDF/TIFF file
        gcs_destination_uri (str): GCS URI prefix for output files
        debug_output_dir (str, optional): Directory to save debug files
        
    Returns:
        dict: A dictionary containing annotation structure information
    """
    text, annotations = async_detect_document(gcs_source_uri, gcs_destination_uri, debug_annotations=True, debug_output_dir=debug_output_dir)
    
    debug_info = {
        "total_pages": len(annotations),
        "sample_annotation_keys": list(annotations[0].keys()) if annotations else [],
        "annotations": annotations
    }
    
    return debug_info

if __name__ == "__main__":
    # Example usage - update these paths as needed
    input_folder = r"./input_pdfs"  # Folder containing PDF files
    output_folder = r"./output_text"  # Folder where text files will be saved
    
    # Create directories if they don't exist
    if not os.path.exists(input_folder):
        os.makedirs(input_folder)
        print(f"Created input folder: {input_folder}")
        print("Please add PDF files to this folder and run again.")
    else:
        # Example of using the traditional method
        print("Processing with traditional method...")
        process_all_pdfs(input_folder, output_folder)
        print("Text extraction completed!")
        
        # Example of using async document detection (now configured!)
        # Uncomment the following lines to use async processing:
        """
        # Configure your GCS bucket name
        bucket_name = "book-scanner-ocr-bucket"
        
        # Process a single PDF with async method
        pdf_files = [f for f in os.listdir(input_folder) if f.endswith(".pdf")]
        if pdf_files:
            pdf_path = os.path.join(input_folder, pdf_files[0])
            print(f"\nProcessing {pdf_path} with async document detection...")
            
            try:
                extracted_text = upload_to_gcs_and_process(pdf_path, bucket_name)
                
                # Save the result
                output_file = os.path.join(output_folder, f"{pdf_files[0]}_async.txt")
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(extracted_text)
                print(f"Async processing completed! Output saved to {output_file}")
                
            except Exception as e:
                print(f"Error with async processing: {e}")
                print("Make sure you have:")
                print("1. A GCS bucket created")
                print("2. Proper authentication set up")
                print("3. google-cloud-storage package installed")
        """