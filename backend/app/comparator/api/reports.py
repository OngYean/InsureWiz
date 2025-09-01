"""
API endpoints for report generation and PDF export
"""

from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import StreamingResponse
from typing import Optional
import logging
from io import BytesIO

from ..services.pdf_generator import pdf_generator
from ..database.operations import comparison_ops
from ..utils.compliance import compliance_manager

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/comparator/reports", tags=["reports"])

@router.get("/pdf/{session_id}")
async def generate_comparison_pdf(session_id: str):
    """Generate PDF report for a comparison session"""
    try:
        # Get comparison session
        session = await comparison_ops.get_comparison_session(session_id)
        
        if not session:
            raise HTTPException(status_code=404, detail="Comparison session not found")
        
        # Check compliance for report generation
        compliance_issues = compliance_manager.validate_report_generation(session)
        if compliance_issues:
            raise HTTPException(
                status_code=400,
                detail=f"Report generation not compliant: {'; '.join(compliance_issues)}"
            )
        
        # Generate PDF
        pdf_buffer = await pdf_generator.generate_comparison_report(session)
        
        if not pdf_buffer:
            raise HTTPException(status_code=500, detail="Failed to generate PDF report")
        
        # Create filename
        timestamp = session.created_at.strftime("%Y%m%d_%H%M%S") if session.created_at else "unknown"
        filename = f"insurance_comparison_{session_id}_{timestamp}.pdf"
        
        # Return PDF as streaming response
        pdf_buffer.seek(0)
        
        return StreamingResponse(
            BytesIO(pdf_buffer.read()),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}",
                "Content-Type": "application/pdf"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating PDF report: {e}")
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")

@router.get("/preview/{session_id}")
async def preview_comparison_report(session_id: str):
    """Generate HTML preview of comparison report"""
    try:
        # Get comparison session
        session = await comparison_ops.get_comparison_session(session_id)
        
        if not session:
            raise HTTPException(status_code=404, detail="Comparison session not found")
        
        # Generate HTML preview
        html_content = await pdf_generator.generate_html_preview(session)
        
        if not html_content:
            raise HTTPException(status_code=500, detail="Failed to generate HTML preview")
        
        # Return HTML content
        return Response(
            content=html_content,
            media_type="text/html",
            headers={
                "Content-Type": "text/html; charset=utf-8"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating HTML preview: {e}")
        raise HTTPException(status_code=500, detail=f"Preview generation failed: {str(e)}")

@router.get("/summary/{session_id}")
async def get_comparison_summary(session_id: str):
    """Get text summary of comparison results"""
    try:
        # Get comparison session
        session = await comparison_ops.get_comparison_session(session_id)
        
        if not session:
            raise HTTPException(status_code=404, detail="Comparison session not found")
        
        # Generate summary
        summary = await pdf_generator.generate_text_summary(session)
        
        return {
            "status": "success",
            "session_id": session_id,
            "summary": summary,
            "total_policies": len(session.ranked_policies),
            "top_recommendation": session.ranked_policies[0].insurer if session.ranked_policies else None,
            "generated_at": session.created_at.isoformat() if session.created_at else None
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating summary: {e}")
        raise HTTPException(status_code=500, detail=f"Summary generation failed: {str(e)}")

@router.post("/email/{session_id}")
async def email_comparison_report(
    session_id: str,
    email_address: str,
    include_pdf: bool = True,
    include_summary: bool = True
):
    """Email comparison report (placeholder implementation)"""
    try:
        # Get comparison session
        session = await comparison_ops.get_comparison_session(session_id)
        
        if not session:
            raise HTTPException(status_code=404, detail="Comparison session not found")
        
        # Validate email address (basic check)
        if "@" not in email_address or "." not in email_address:
            raise HTTPException(status_code=400, detail="Invalid email address")
        
        # Check compliance for email sending
        compliance_issues = compliance_manager.validate_email_sending(session, email_address)
        if compliance_issues:
            raise HTTPException(
                status_code=400,
                detail=f"Email sending not compliant: {'; '.join(compliance_issues)}"
            )
        
        # TODO: Implement actual email sending
        # This would integrate with an email service like SendGrid, AWS SES, etc.
        
        return {
            "status": "success",
            "message": f"Report sent to {email_address}",
            "session_id": session_id,
            "includes": {
                "pdf_attachment": include_pdf,
                "summary_text": include_summary
            },
            "note": "Email functionality is placeholder - integration with email service required"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error sending email report: {e}")
        raise HTTPException(status_code=500, detail=f"Email sending failed: {str(e)}")

@router.get("/formats")
async def get_supported_formats():
    """Get list of supported report formats"""
    return {
        "status": "success",
        "supported_formats": [
            {
                "format": "PDF",
                "description": "Professional PDF report with charts and tables",
                "endpoint": "/pdf/{session_id}",
                "content_type": "application/pdf"
            },
            {
                "format": "HTML Preview",
                "description": "HTML preview of the report for web viewing",
                "endpoint": "/preview/{session_id}",
                "content_type": "text/html"
            },
            {
                "format": "Text Summary",
                "description": "JSON response with text summary",
                "endpoint": "/summary/{session_id}",
                "content_type": "application/json"
            },
            {
                "format": "Email",
                "description": "Email delivery with PDF attachment",
                "endpoint": "/email/{session_id}",
                "content_type": "application/json"
            }
        ]
    }

@router.get("/templates")
async def get_report_templates():
    """Get available report templates"""
    try:
        templates = await pdf_generator.get_available_templates()
        
        return {
            "status": "success",
            "templates": templates
        }
        
    except Exception as e:
        logger.error(f"Error getting templates: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve templates: {str(e)}")

@router.post("/custom/{session_id}")
async def generate_custom_report(
    session_id: str,
    template_name: Optional[str] = "default",
    include_sections: Optional[list] = None,
    custom_styling: Optional[dict] = None
):
    """Generate custom report with specific template and sections"""
    try:
        # Get comparison session
        session = await comparison_ops.get_comparison_session(session_id)
        
        if not session:
            raise HTTPException(status_code=404, detail="Comparison session not found")
        
        # Generate custom report
        pdf_buffer = await pdf_generator.generate_custom_report(
            session=session,
            template_name=template_name,
            include_sections=include_sections or ["all"],
            custom_styling=custom_styling or {}
        )
        
        if not pdf_buffer:
            raise HTTPException(status_code=500, detail="Failed to generate custom report")
        
        # Create filename
        timestamp = session.created_at.strftime("%Y%m%d_%H%M%S") if session.created_at else "unknown"
        filename = f"custom_insurance_report_{session_id}_{timestamp}.pdf"
        
        # Return PDF as streaming response
        pdf_buffer.seek(0)
        
        return StreamingResponse(
            BytesIO(pdf_buffer.read()),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}",
                "Content-Type": "application/pdf"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating custom report: {e}")
        raise HTTPException(status_code=500, detail=f"Custom report generation failed: {str(e)}")
