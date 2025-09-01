"""
PDF report generation service using Jinja2 templates and WeasyPrint
"""

import os
import logging
from typing import Optional, Dict, Any
from datetime import datetime
from pathlib import Path
import tempfile
import uuid

from jinja2 import Environment, FileSystemLoader, select_autoescape
from ..models.comparison import ComparisonResult, PDFReportRequest, PDFReportResponse
from ..utils.compliance import compliance_manager

logger = logging.getLogger(__name__)

class PDFGenerator:
    """Service for generating PDF comparison reports"""
    
    def __init__(self):
        # Setup template environment
        template_dir = Path(__file__).parent.parent / "templates"
        self.jinja_env = Environment(
            loader=FileSystemLoader(str(template_dir)),
            autoescape=select_autoescape(['html', 'xml'])
        )
        
        # Setup output directory
        self.output_dir = Path("reports/generated")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"PDF Generator initialized. Template dir: {template_dir}, Output dir: {self.output_dir}")
    
    def generate_comparison_report(self, comparison_result: ComparisonResult, request: PDFReportRequest) -> PDFReportResponse:
        """Generate PDF comparison report"""
        try:
            report_id = str(uuid.uuid4())
            logger.info(f"Generating PDF report {report_id} for session {comparison_result.session_id}")
            
            # Prepare template data
            template_data = self._prepare_template_data(comparison_result, request)
            
            # Render HTML
            html_content = self._render_html_template(template_data)
            
            # Generate PDF (stub implementation)
            pdf_path = self._generate_pdf_from_html(html_content, report_id)
            
            # Create response
            response = PDFReportResponse(
                report_id=report_id,
                pdf_path=str(pdf_path),
                generated_at=datetime.now(),
                expires_at=datetime.now().replace(hour=23, minute=59, second=59),  # End of day
                file_size=self._get_file_size(pdf_path) if pdf_path.exists() else None
            )
            
            logger.info(f"PDF report generated successfully: {report_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error generating PDF report: {e}")
            raise
    
    def _prepare_template_data(self, comparison_result: ComparisonResult, request: PDFReportRequest) -> Dict[str, Any]:
        """Prepare data for template rendering"""
        # Get top 5 recommendations for detailed display
        top_recommendations = comparison_result.recommendations[:5]
        
        # Prepare comparison matrix for top policies
        matrix_data = self._prepare_matrix_data(comparison_result.matrix, top_recommendations)
        
        template_data = {
            # Report metadata
            "report_id": request.session_id,
            "generated_date": datetime.now().strftime("%d %B %Y"),
            "generated_time": datetime.now().strftime("%I:%M %p"),
            
            # Customer information
            "customer_name": comparison_result.customer_name,
            "comparison_date": comparison_result.comparison_date.strftime("%d %B %Y"),
            
            # Results
            "total_policies": comparison_result.summary.total_policies_compared,
            "top_recommendation": comparison_result.summary.top_recommendation,
            "recommendations": top_recommendations,
            "summary": comparison_result.summary,
            
            # Matrix data
            "matrix": matrix_data,
            "include_detailed_matrix": request.include_detailed_matrix,
            
            # Analysis
            "market_insights": comparison_result.market_insights,
            "general_recommendations": comparison_result.general_recommendations,
            "next_steps": comparison_result.next_steps,
            
            # Compliance
            "disclaimer": comparison_result.disclaimer,
            "compliance_notes": comparison_result.compliance_notes,
            "data_sources": comparison_result.data_sources[:10],  # Limit to 10 sources
            
            # Branding
            "branding": request.branding or self._get_default_branding(),
            "custom_notes": request.custom_notes,
            
            # Data freshness
            "data_freshness": self._format_data_freshness(comparison_result.data_freshness),
            
            # Processing info
            "processing_time": f"{comparison_result.processing_time:.2f} seconds" if comparison_result.processing_time else "N/A",
            "ai_model": comparison_result.ai_model_used or "N/A"
        }
        
        return template_data
    
    def _prepare_matrix_data(self, matrix, top_recommendations) -> Dict[str, Any]:
        """Prepare comparison matrix data for template"""
        if not top_recommendations:
            return {"insurers": [], "features": [], "data": {}}
        
        # Get insurers from top recommendations
        insurers = [rec.policy.insurer for rec in top_recommendations]
        
        # Core features to display
        core_features = [
            "Coverage Type", "Takaful", "Flood Coverage", "Theft Coverage",
            "Windscreen", "Personal Accident", "24/7 Roadside", "Digital Claims",
            "Mobile App", "NCD Protection", "Key Replacement", "Courtesy Car"
        ]
        
        # Build matrix data
        matrix_data = {}
        for insurer in insurers:
            if insurer in matrix.matrix:
                matrix_data[insurer] = {}
                for feature in core_features:
                    matrix_data[insurer][feature] = matrix.matrix[insurer].get(feature, "N/A")
        
        return {
            "insurers": insurers,
            "features": core_features,
            "data": matrix_data,
            "best_coverage": matrix.best_coverage,
            "best_service": matrix.best_service,
            "best_value": matrix.best_value
        }
    
    def _render_html_template(self, template_data: Dict[str, Any]) -> str:
        """Render HTML template with data"""
        try:
            template = self.jinja_env.get_template("comparison.html")
            html_content = template.render(**template_data)
            
            logger.debug("HTML template rendered successfully")
            return html_content
            
        except Exception as e:
            logger.error(f"Error rendering HTML template: {e}")
            # Fallback to simple HTML
            return self._create_fallback_html(template_data)
    
    def _generate_pdf_from_html(self, html_content: str, report_id: str) -> Path:
        """Generate PDF from HTML content (stub implementation)"""
        # Note: This is a stub implementation
        # In production, you would use WeasyPrint or similar:
        # from weasyprint import HTML
        # HTML(string=html_content).write_pdf(pdf_path)
        
        pdf_filename = f"comparison_report_{report_id}.pdf"
        pdf_path = self.output_dir / pdf_filename
        
        try:
            # For now, save as HTML file (stub)
            html_path = self.output_dir / f"comparison_report_{report_id}.html"
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            # Create a placeholder PDF file
            with open(pdf_path, 'w') as f:
                f.write(f"PDF Report Placeholder\nReport ID: {report_id}\nGenerated: {datetime.now()}\n")
            
            logger.info(f"PDF generated (stub): {pdf_path}")
            return pdf_path
            
        except Exception as e:
            logger.error(f"Error generating PDF: {e}")
            raise
    
    def _create_fallback_html(self, template_data: Dict[str, Any]) -> str:
        """Create fallback HTML when template fails"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Insurance Comparison Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .header {{ text-align: center; margin-bottom: 30px; }}
                .section {{ margin-bottom: 20px; }}
                table {{ width: 100%; border-collapse: collapse; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Motor Insurance Comparison Report</h1>
                <p>Customer: {template_data.get('customer_name', 'N/A')}</p>
                <p>Generated: {template_data.get('generated_date', 'N/A')}</p>
            </div>
            
            <div class="section">
                <h2>Summary</h2>
                <p>Total policies compared: {template_data.get('total_policies', 0)}</p>
                <p>Top recommendation: {template_data.get('top_recommendation', 'N/A')}</p>
            </div>
            
            <div class="section">
                <h2>Top Recommendations</h2>
                <ol>
                    {''.join([f"<li>{rec.policy.insurer} - {rec.policy.product_name}</li>" for rec in template_data.get('recommendations', [])[:3]])}
                </ol>
            </div>
            
            <div class="section">
                <h2>Disclaimer</h2>
                <p>{template_data.get('disclaimer', 'Standard insurance disclaimer.')}</p>
            </div>
        </body>
        </html>
        """
    
    def _get_default_branding(self) -> Dict[str, str]:
        """Get default branding configuration"""
        return {
            "company_name": "InsureWiz",
            "logo_url": "",
            "primary_color": "#2563eb",
            "secondary_color": "#64748b",
            "footer_text": "Powered by InsureWiz AI Insurance Comparison Platform"
        }
    
    def _format_data_freshness(self, freshness_data: Dict[str, datetime]) -> Dict[str, str]:
        """Format data freshness for display"""
        formatted = {}
        
        for insurer, last_checked in freshness_data.items():
            days_ago = (datetime.now() - last_checked).days
            if days_ago == 0:
                formatted[insurer] = "Today"
            elif days_ago == 1:
                formatted[insurer] = "Yesterday"
            elif days_ago <= 7:
                formatted[insurer] = f"{days_ago} days ago"
            elif days_ago <= 30:
                weeks = days_ago // 7
                formatted[insurer] = f"{weeks} week{'s' if weeks > 1 else ''} ago"
            else:
                formatted[insurer] = last_checked.strftime("%d %b %Y")
        
        return formatted
    
    def _get_file_size(self, file_path: Path) -> Optional[int]:
        """Get file size in bytes"""
        try:
            return file_path.stat().st_size
        except OSError:
            return None
    
    def get_report_url(self, report_id: str) -> Optional[str]:
        """Get URL for downloading generated report"""
        # In production, this would return a proper download URL
        pdf_path = self.output_dir / f"comparison_report_{report_id}.pdf"
        
        if pdf_path.exists():
            return f"/api/comparator/reports/download/{report_id}"
        
        return None
    
    def cleanup_old_reports(self, days_to_keep: int = 30):
        """Clean up old report files"""
        cutoff_time = datetime.now().timestamp() - (days_to_keep * 24 * 3600)
        
        cleaned_count = 0
        for file_path in self.output_dir.glob("comparison_report_*.pdf"):
            try:
                if file_path.stat().st_mtime < cutoff_time:
                    file_path.unlink()
                    cleaned_count += 1
            except OSError:
                continue
        
        logger.info(f"Cleaned up {cleaned_count} old report files")

# Global instance
pdf_generator = PDFGenerator()
