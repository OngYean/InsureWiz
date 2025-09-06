#!/usr/bin/env python3

try:
    import weasyprint
    print("WeasyPrint is available!")
    
    # Test basic PDF generation
    html_content = """
    <!DOCTYPE html>
    <html>
    <head><title>Test</title></head>
    <body><h1>Test PDF Generation</h1><p>This is a test.</p></body>
    </html>
    """
    
    pdf_bytes = weasyprint.HTML(string=html_content).write_pdf()
    print(f"PDF generated successfully! Size: {len(pdf_bytes)} bytes")
    
except ImportError as e:
    print(f"WeasyPrint import error: {e}")
except Exception as e:
    print(f"PDF generation error: {e}")
