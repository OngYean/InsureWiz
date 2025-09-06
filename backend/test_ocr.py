#!/usr/bin/env python3
"""
Test script to verify OCR fallback functionality
"""
import sys
import os
import io

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.ml.llm_insights import extract_text_from_pdf

def test_pdf_extraction():
    """Test PDF text extraction with both direct and OCR methods."""
    
    # Test with existing policy.txt file converted to a simple test
    try:
        # Try to read an existing PDF file
        pdf_files = ['policy.txt', 'empty.txt']
        
        for filename in pdf_files:
            if os.path.exists(filename):
                print(f"\n=== Testing {filename} ===")
                
                # Read file content
                with open(filename, 'rb') as f:
                    file_content = f.read()
                
                # Create BytesIO object
                pdf_file = io.BytesIO(file_content)
                
                # Test extraction
                extracted_text = extract_text_from_pdf(pdf_file)
                
                print(f"Extracted text length: {len(extracted_text)}")
                if extracted_text:
                    print(f"First 200 characters: {extracted_text[:200]}...")
                else:
                    print("No text extracted")
                    
    except Exception as e:
        print(f"Error during testing: {e}")

if __name__ == "__main__":
    test_pdf_extraction()
