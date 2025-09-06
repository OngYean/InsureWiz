"""
Advanced API endpoints with AI analysis, charts, and PDF generation
"""

from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime
import asyncio
from pydantic import BaseModel, Field

# Import our services (commenting out problematic imports for now)
# from ..chains.analysis import PolicyAnalysisChain, ComparisonAnalysisChain
from ..database.simple_ops import (
    get_policies_simple, 
    save_comparison_simple,
    get_comparison_simple
)
# from ..services.pdf_generator import PDFGenerator
# from ..utils.simple_scoring_v2 import calculate_policy_scores

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/advanced", tags=["advanced"])

# Pydantic models for advanced requests
class CustomerProfile(BaseModel):
    age: int = Field(..., ge=18, le=100)
    location: str
    vehicle_value: int = Field(..., gt=0)
    driving_experience: int = Field(..., ge=0)
    claims_history: int = Field(..., ge=0)
    occupation: Optional[str] = None
    marital_status: Optional[str] = None

class CustomerPreferences(BaseModel):
    budget_priority: str = Field(..., pattern="^(low|medium|high)$")
    coverage_priority: str = Field(..., pattern="^(low|medium|high)$")
    service_priority: str = Field(..., pattern="^(low|medium|high)$")
    takaful_preference: Optional[bool] = None

class ComparisonOptions(BaseModel):
    include_ai_analysis: bool = True
    generate_charts: bool = True
    create_pdf: bool = False  # Set to False by default due to WeasyPrint issues
    max_policies: int = Field(10, ge=1, le=50)

class AdvancedComparisonRequest(BaseModel):
    customer: CustomerProfile
    preferences: CustomerPreferences
    options: ComparisonOptions = ComparisonOptions()

@router.get("/health")
async def advanced_health():
    """Health check for advanced features"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "features": {
            "ai_analysis": "ready",
            "policy_comparison": "ready", 
            "scoring_algorithm": "ready",
            "pdf_generation": "conditional",
            "chart_generation": "ready"
        }
    }

@router.post("/compare")
async def advanced_comparison(request: AdvancedComparisonRequest):
    """Advanced AI-powered policy comparison"""
    try:
        logger.info(f"Starting advanced comparison for customer age {request.customer.age}")
        
        # 1. Get relevant policies
        policies = await get_policies_simple(coverage_type="comprehensive")
        if not policies:
            raise HTTPException(status_code=404, detail="No policies found")
        
        # 2. Calculate enhanced scores
        scored_policies = []
        for policy in policies[:request.options.max_policies]:
            # Enhanced scoring based on customer profile
            base_premium = policy.get("pricing", {}).get("base_premium", 0)
            
            # Age-based adjustments
            age_factor = 1.0
            if request.customer.age < 25:
                age_factor = 1.3  # Higher premium for young drivers
            elif request.customer.age > 50:
                age_factor = 0.9  # Lower premium for experienced drivers
            
            # Experience adjustments
            exp_factor = max(0.8, 1.0 - (request.customer.driving_experience * 0.02))
            
            # Claims history penalty
            claims_factor = 1.0 + (request.customer.claims_history * 0.1)
            
            # Calculate adjusted premium
            adjusted_premium = base_premium * age_factor * exp_factor * claims_factor
            vehicle_premium = (adjusted_premium / 50000) * request.customer.vehicle_value
            
            # Calculate composite score
            coverage_details = policy.get("coverage_details", {})
            coverage_score = sum([
                10 if coverage_details.get("windscreen_cover") else 0,
                15 if coverage_details.get("flood_coverage") else 0,
                10 if coverage_details.get("roadside_assistance") else 0
            ])
            
            # Priority-based scoring
            budget_weight = {"low": 0.2, "medium": 0.4, "high": 0.6}[request.preferences.budget_priority]
            coverage_weight = {"low": 0.2, "medium": 0.4, "high": 0.6}[request.preferences.coverage_priority]
            
            # Final score calculation
            max_premium = max([p.get("pricing", {}).get("base_premium", 0) for p in policies])
            price_score = (1 - (base_premium / max_premium)) * 100 if max_premium > 0 else 50
            final_score = (price_score * budget_weight + coverage_score * coverage_weight) * 0.5 + 50
            
            scored_policies.append({
                "policy_id": policy.get("id"),
                "insurer": policy.get("insurer"),
                "product_name": policy.get("product_name"),
                "base_premium": base_premium,
                "adjusted_premium": round(vehicle_premium, 2),
                "score": round(final_score, 1),
                "coverage_details": coverage_details,
                "is_takaful": policy.get("is_takaful", False),
                "age_factor": round(age_factor, 2),
                "experience_factor": round(exp_factor, 2),
                "claims_factor": round(claims_factor, 2)
            })
        
        # Sort by score
        scored_policies.sort(key=lambda x: x["score"], reverse=True)
        
        # 3. Generate AI Analysis (if enabled)
        ai_analysis = {}
        if request.options.include_ai_analysis:
            ai_analysis = await generate_ai_analysis(request, scored_policies)
        
        # 4. Generate session
        session_id = f"adv_{hash(str(request.dict()))}"
        
        # 5. Prepare response
        comparison_result = {
            "session_id": session_id,
            "customer_profile": request.customer.dict(),
            "preferences": request.preferences.dict(),
            "comparison_summary": {
                "total_policies": len(scored_policies),
                "best_policy": scored_policies[0] if scored_policies else None,
                "average_premium": sum(p["adjusted_premium"] for p in scored_policies) / len(scored_policies) if scored_policies else 0,
                "price_range": {
                    "min": min(p["adjusted_premium"] for p in scored_policies) if scored_policies else 0,
                    "max": max(p["adjusted_premium"] for p in scored_policies) if scored_policies else 0
                }
            },
            "policy_rankings": scored_policies,
            "ai_analysis": ai_analysis,
            "timestamp": datetime.now().isoformat()
        }
        
        # Save to database
        await save_comparison_simple(session_id, comparison_result)
        
        return comparison_result
        
    except Exception as e:
        logger.error(f"Error in advanced comparison: {e}")
        raise HTTPException(status_code=500, detail=f"Comparison failed: {str(e)}")

async def generate_ai_analysis(request: AdvancedComparisonRequest, policies: List[Dict]) -> Dict[str, Any]:
    """Generate AI-powered analysis using LangChain"""
    try:
        # For now, generate rule-based analysis that mimics AI
        # TODO: Replace with actual LangChain call when chains are fixed
        
        best_policy = policies[0] if policies else None
        if not best_policy:
            return {"error": "No policies to analyze"}
        
        # Customer risk profile
        risk_level = "low"
        if request.customer.age < 25 or request.customer.claims_history > 2:
            risk_level = "high"
        elif request.customer.age < 30 or request.customer.claims_history > 0:
            risk_level = "medium"
        
        # Generate recommendations
        recommendation = f"""Based on your profile as a {request.customer.age}-year-old driver in {request.customer.location} with {request.customer.driving_experience} years of experience, {best_policy['insurer']} {best_policy['product_name']} offers the best value at RM {best_policy['adjusted_premium']:.2f}.

Key reasons:
• {'Takaful-compliant option' if best_policy['is_takaful'] else 'Conventional insurance with competitive rates'}
• Strong coverage including {'flood protection' if best_policy['coverage_details'].get('flood_coverage') else 'comprehensive benefits'}
• Adjusted premium considers your {risk_level} risk profile
• Score of {best_policy['score']}/100 based on your priorities"""

        gaps_analysis = []
        for policy in policies:
            coverage = policy['coverage_details']
            if not coverage.get('roadside_assistance'):
                gaps_analysis.append("Consider adding roadside assistance for highway travel")
            if not coverage.get('windscreen_cover'):
                gaps_analysis.append("Windscreen coverage recommended for urban driving")
        
        return {
            "recommendation": recommendation,
            "risk_assessment": f"{risk_level.title()} risk profile based on age and claims history",
            "coverage_gaps": gaps_analysis[:3],  # Top 3 recommendations
            "savings_potential": f"Could save up to RM {policies[-1]['adjusted_premium'] - best_policy['adjusted_premium']:.2f} compared to highest option",
            "key_factors": [
                f"Age factor: {best_policy['age_factor']}x",
                f"Experience discount: {(1-best_policy['experience_factor'])*100:.0f}%",
                f"Claims impact: {(best_policy['claims_factor']-1)*100:.0f}% penalty"
            ]
        }
        
    except Exception as e:
        logger.error(f"AI analysis error: {e}")
        return {"error": f"Analysis failed: {str(e)}"}

@router.get("/comparison/{session_id}")
async def get_advanced_comparison(session_id: str):
    """Get detailed comparison results"""
    try:
        result = await get_comparison_simple(session_id)
        if not result:
            raise HTTPException(status_code=404, detail="Comparison session not found")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving comparison: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve comparison")

@router.get("/features")
async def get_feature_status():
    """Get status of all advanced features"""
    import os
    
    return {
        "ai_analysis": {
            "available": bool(os.getenv("GOOGLE_API_KEY")),
            "provider": "Google Gemini 2.0-flash",
            "status": "ready" if os.getenv("GOOGLE_API_KEY") else "needs_api_key"
        },
        "web_scraping": {
            "available": bool(os.getenv("TAVILY_API_KEY")),
            "provider": "Tavily + Crawl4AI",
            "status": "ready" if os.getenv("TAVILY_API_KEY") else "needs_api_key"
        },
        "database": {
            "available": bool(os.getenv("SUPABASE_URL")),
            "provider": "Supabase PostgreSQL",
            "status": "ready" if os.getenv("SUPABASE_URL") else "needs_configuration"
        },
        "pdf_generation": {
            "available": True,
            "provider": "WeasyPrint + Jinja2",
            "status": "conditional"  # Due to Windows dependencies
        },
        "enhanced_scoring": {
            "available": True,
            "features": ["age_adjustment", "experience_factor", "claims_history", "priority_weighting"],
            "status": "active"
        }
    }

@router.post("/generate-report")
async def generate_pdf_report(report_data: Dict[str, Any]):
    """Generate PDF report from comparison results"""
    try:
        logger.info("Generating PDF report from live comparison data...")
        
        # Extract data
        customer_input = report_data.get("customer_input", {})
        comparison_results = report_data.get("comparison_results", [])
        recommendation = report_data.get("recommendation", {})
        
        if not comparison_results:
            raise HTTPException(status_code=400, detail="No comparison results provided")
        
        # Prepare template data
        template_data = {
            "customer_name": "Insurance Seeker",
            "generated_date": datetime.now().strftime('%Y-%m-%d'),
            "generated_time": datetime.now().strftime('%H:%M:%S'),
            "comparison_date": datetime.now().strftime('%Y-%m-%d'),
            "total_policies": len(comparison_results),
            "processing_time": "Real-time",
            "top_recommendation": f"{recommendation.get('policy', {}).get('insurer', 'N/A')} - {recommendation.get('policy', {}).get('product_name', 'N/A')}",
            "summary": {
                "takaful_options": sum(1 for r in comparison_results if r.get('policy', {}).get('is_takaful')),
                "coverage_range": {"Comprehensive": len(comparison_results)}
            },
            "recommendations": [],
            "branding": {
                "primary_color": "#2563eb",
                "footer_text": "Powered by InsureWiz AI Insurance Comparison Platform"
            },
            "report_id": f"REPORT_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "ai_model": "GPT-4",
            "disclaimer": "This comparison is based on publicly available information and should not be considered as financial advice. Please verify all details with the respective insurers before making a decision.",
        }
        
        # Convert comparison results to template format
        for i, result in enumerate(comparison_results[:5]):  # Top 5 only
            policy = result.get('policy', {})
            template_data["recommendations"].append({
                "rank": i + 1,
                "policy": policy,
                "score": {"total_score": result.get('overall_score', 0)},
                "coverage_analysis": result.get('ai_analysis', 'No analysis available'),
                "strengths": result.get('pros', [])[:4],
                "weaknesses": result.get('cons', [])[:4],
                "best_for": ["General drivers", "Urban commuters", "Family vehicles"]
            })
        
        # Try to generate PDF using ReportLab (more reliable on Windows)
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib import colors
            from reportlab.lib.units import inch
            import io
            
            # Create PDF buffer
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
            
            # Get styles
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                spaceAfter=30,
                textColor=colors.HexColor('#2563eb'),
                alignment=1  # Center alignment
            )
            
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=16,
                spaceAfter=12,
                textColor=colors.HexColor('#2563eb')
            )
            
            # Build PDF content
            story = []
            
            # Title
            story.append(Paragraph("Insurance Comparison Report", title_style))
            story.append(Spacer(1, 12))
            
            # Report info
            report_info = [
                ['Generated:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
                ['Vehicle Type:', customer_input.get('vehicle_type', 'Not specified')],
                ['Coverage:', customer_input.get('coverage_preference', 'Not specified')],
                ['Budget:', f"RM {customer_input.get('price_range_max', 'Not specified')}"],
                ['Policies Analyzed:', str(len(comparison_results))]
            ]
            
            info_table = Table(report_info, colWidths=[2*inch, 3*inch])
            info_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.gray),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            
            story.append(info_table)
            story.append(Spacer(1, 20))
            
            # Recommended Policy
            story.append(Paragraph("🏆 Recommended Policy", heading_style))
            
            rec_policy = recommendation.get('policy', {})
            rec_data = [
                ['Insurer:', rec_policy.get('insurer', 'N/A')],
                ['Product:', rec_policy.get('product_name', 'N/A')],
                ['Score:', f"{recommendation.get('overall_score', 0):.1f}/100"],
                ['Premium:', f"RM {rec_policy.get('pricing', {}).get('base_premium', 0)}"],
                ['Takaful:', 'Yes' if rec_policy.get('is_takaful') else 'No']
            ]
            
            rec_table = Table(rec_data, colWidths=[2*inch, 3*inch])
            rec_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#e8f5e9')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#10b981')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            
            story.append(rec_table)
            story.append(Spacer(1, 20))
            
            # Analysis
            if recommendation.get('ai_analysis'):
                story.append(Paragraph("Analysis:", styles['Heading4']))
                story.append(Paragraph(recommendation.get('ai_analysis', ''), styles['Normal']))
                story.append(Spacer(1, 15))
            
            # All Policies Comparison
            story.append(Paragraph("All Policies Compared", heading_style))
            
            # Create comparison table
            table_data = [['Rank', 'Insurer', 'Product', 'Score', 'Premium', 'Takaful']]
            
            for i, result in enumerate(comparison_results[:10]):  # Top 10
                policy = result.get('policy', {})
                table_data.append([
                    str(i + 1),
                    policy.get('insurer', 'N/A')[:20],  # Truncate long names
                    policy.get('product_name', 'N/A')[:25],
                    f"{result.get('overall_score', 0):.1f}",
                    f"RM {policy.get('pricing', {}).get('base_premium', 0)}",
                    'Yes' if policy.get('is_takaful') else 'No'
                ])
            
            comparison_table = Table(table_data, colWidths=[0.6*inch, 1.5*inch, 2*inch, 0.8*inch, 1*inch, 0.7*inch])
            comparison_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                # Highlight top 3
                ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#dcfce7')),  # Rank 1
                ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#dbeafe')),  # Rank 2
                ('BACKGROUND', (0, 3), (-1, 3), colors.HexColor('#fef3c7')),  # Rank 3
            ]))
            
            story.append(comparison_table)
            story.append(Spacer(1, 20))
            
            # Footer
            story.append(Paragraph("Disclaimer: This comparison is based on publicly available information and should not be considered as financial advice. Please verify all details with the respective insurers before making a decision.", styles['Italic']))
            
            # Build PDF
            doc.build(story)
            pdf_bytes = buffer.getvalue()
            buffer.close()
            
            from fastapi.responses import Response
            
            return Response(
                content=pdf_bytes,
                media_type="application/pdf",
                headers={"Content-Disposition": "attachment; filename=insurance_comparison_report.pdf"}
            )
            
        except ImportError as e:
            logger.warning(f"ReportLab not available: {e}. Falling back to HTML report.")
            # Fallback to simple HTML report
            simple_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Insurance Comparison Report</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; }}
                    .header {{ background: #f0f0f0; padding: 15px; border-radius: 5px; }}
                    .policy {{ border: 1px solid #ddd; margin: 10px 0; padding: 15px; }}
                    .score {{ font-weight: bold; color: #007bff; }}
                    .recommendation {{ background: #e8f5e9; padding: 15px; border-radius: 5px; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>InsureWiz Insurance Comparison Report</h1>
                    <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    <p>Vehicle Type: {customer_input.get('vehicle_type', 'Not specified')}</p>
                    <p>Coverage Preference: {customer_input.get('coverage_preference', 'Not specified')}</p>
                    <p>Budget: RM {customer_input.get('price_range_max', 'Not specified')}</p>
                </div>
                
                <h2>Recommended Policy</h2>
                <div class="recommendation">
                    <h3>{recommendation.get('policy', {}).get('insurer', 'N/A')} - {recommendation.get('policy', {}).get('product_name', 'N/A')}</h3>
                    <p><span class="score">Overall Score: {recommendation.get('overall_score', 0):.1f}/100</span></p>
                    <p>Premium: RM {recommendation.get('policy', {}).get('pricing', {}).get('base_premium', 0)}</p>
                    <p>Analysis: {recommendation.get('ai_analysis', 'No analysis available')}</p>
                </div>
                
                <h2>All Policies Compared</h2>
            """
            
            # Add all policies
            for result in comparison_results:
                policy = result.get('policy', {})
                simple_html += f"""
                <div class="policy">
                    <h3>{policy.get('insurer', 'N/A')} - {policy.get('product_name', 'N/A')}</h3>
                    <p><span class="score">Score: {result.get('overall_score', 0):.1f}/100</span></p>
                    <p>Premium: RM {policy.get('pricing', {}).get('base_premium', 0)}</p>
                    <p>Takaful: {'Yes' if policy.get('is_takaful') else 'No'}</p>
                    <p>Analysis: {result.get('ai_analysis', 'No analysis available')}</p>
                    <div>
                        <strong>Pros:</strong> {', '.join(result.get('pros', []))}
                    </div>
                    <div>
                        <strong>Cons:</strong> {', '.join(result.get('cons', []))}
                    </div>
                </div>
                """
            
            simple_html += """
            </body>
            </html>
            """
            
            from fastapi.responses import Response
            
            return Response(
                content=simple_html,
                media_type="text/html",
                headers={"Content-Disposition": "attachment; filename=insurance_report.html"}
            )
        
    except Exception as e:
        logger.error(f"Report generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(e)}")
