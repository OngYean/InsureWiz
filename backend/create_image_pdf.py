#!/usr/bin/env python3
"""
Create a PDF with text rendered as images to test OCR functionality
"""
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PIL import Image, ImageDraw, ImageFont
import io

def create_image_based_pdf():
    """Create a PDF with text rendered as images to force OCR usage."""
    buffer = io.BytesIO()
    
    # Create an image with text
    img_width, img_height = 500, 600
    img = Image.new('RGB', (img_width, img_height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Try to use a system font, fallback to default
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
        font_text = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
    except:
        font_title = ImageFont.load_default()
        font_text = ImageFont.load_default()
    
    # Draw text on image
    y_pos = 30
    draw.text((20, y_pos), "MOTOR INSURANCE POLICY", fill='black', font=font_title)
    
    y_pos += 50
    policy_lines = [
        "Policy Number: IMG123456789",
        "",
        "This is a scanned policy document.",
        "Coverage includes:",
        "- Comprehensive coverage",
        "- Collision damage",
        "- Third party liability",
        "",
        "Claims must be reported within 24 hours.",
        "Deductible applies to all claims.",
        "",
        "This document tests OCR functionality."
    ]
    
    for line in policy_lines:
        if line.strip():
            draw.text((20, y_pos), line, fill='black', font=font_text)
        y_pos += 25
    
    # Save image temporarily
    img_buffer = io.BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    
    # Create PDF with the image
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Add the image to PDF
    c.drawInlineImage(img_buffer, 50, height-650, width=400, height=500)
    c.save()
    
    buffer.seek(0)
    
    # Save to file
    with open('image_based_policy.pdf', 'wb') as f:
        f.write(buffer.getvalue())
    
    print("Image-based PDF created: image_based_policy.pdf")
    return buffer

if __name__ == "__main__":
    create_image_based_pdf()
