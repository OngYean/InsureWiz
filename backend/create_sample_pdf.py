#!/usr/bin/env python3
"""
Create a sample PDF with text to test OCR functionality
"""
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

def create_sample_pdf():
    """Create a sample PDF with insurance policy text."""
    buffer = io.BytesIO()
    
    # Create PDF
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Add title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Motor Insurance Policy")
    
    # Add policy content
    c.setFont("Helvetica", 12)
    y_position = height - 100
    
    policy_text = [
        "Policy Number: POL123456789",
        "",
        "Coverage Details:",
        "• Comprehensive Coverage: Included",
        "• Third Party Liability: Up to $1,000,000",
        "• Collision Coverage: Up to actual cash value",
        "• Deductible: $500 for comprehensive, $250 for collision",
        "",
        "Exclusions:",
        "• Damage caused by intentional acts",
        "• Racing or competitive driving",
        "• Driving under the influence",
        "",
        "Claims Process:",
        "• Report claims within 24 hours",
        "• Provide all necessary documentation",
        "• Cooperate with claim investigation"
    ]
    
    for line in policy_text:
        c.drawString(50, y_position, line)
        y_position -= 20
    
    c.save()
    buffer.seek(0)
    
    # Save to file
    with open('sample_policy.pdf', 'wb') as f:
        f.write(buffer.getvalue())
    
    print("Sample PDF created: sample_policy.pdf")
    return buffer

if __name__ == "__main__":
    create_sample_pdf()
