#!/usr/bin/env python3

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph
    from reportlab.lib.styles import getSampleStyleSheet
    import io
    
    print("ReportLab is available!")
    
    # Test basic PDF generation
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    
    story = []
    story.append(Paragraph("Test PDF Generation", styles['Title']))
    story.append(Paragraph("This is a test using ReportLab.", styles['Normal']))
    
    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    print(f"PDF generated successfully! Size: {len(pdf_bytes)} bytes")
    
    # Save test file
    with open("test_report.pdf", "wb") as f:
        f.write(pdf_bytes)
    print("Test PDF saved as test_report.pdf")
    
except ImportError as e:
    print(f"ReportLab import error: {e}")
except Exception as e:
    print(f"PDF generation error: {e}")
