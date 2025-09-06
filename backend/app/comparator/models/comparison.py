"""
Comparison result models for policy analysis and recommendations
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator
from datetime import datetime


class PolicyScore(BaseModel):
    """Individual scoring components for a policy"""
    coverage_score: float = Field(..., description="Coverage breadth score (0-100)")
    service_score: float = Field(..., description="Service quality score (0-100)")
    takaful_score: float = Field(..., description="Takaful preference score (0-100)")
    pricing_score: float = Field(..., description="Pricing attractiveness score (0-100)")
    eligibility_score: float = Field(..., description="Eligibility match score (0-100)")
    total_score: float = Field(..., description="Weighted total score (0-100)")
    
    # Detailed breakdowns
    coverage_details: Dict[str, Any] = Field(default_factory=dict, description="Coverage scoring details")
    service_details: Dict[str, Any] = Field(default_factory=dict, description="Service scoring details")
    pricing_details: Dict[str, Any] = Field(default_factory=dict, description="Pricing scoring details")


class PolicyRecommendation(BaseModel):
    """A policy recommendation with reasoning"""
    policy: Dict[str, Any] = Field(..., description="The policy record")
    rank: int = Field(..., description="Recommendation rank (1-based)")
    score: Dict[str, Any] = Field(..., description="Detailed scoring")
    
    # AI-generated reasoning
    strengths: List[str] = Field(default_factory=list, description="Policy strengths")
    weaknesses: List[str] = Field(default_factory=list, description="Policy limitations")
    best_for: List[str] = Field(default_factory=list, description="Best suited for scenarios")
    key_features: List[str] = Field(default_factory=list, description="Key differentiating features")
    
    # Detailed analysis
    coverage_analysis: str = Field(default="", description="Coverage analysis")
    service_analysis: str = Field(default="", description="Service level analysis")
    value_analysis: str = Field(default="", description="Value for money analysis")
    
    # Compliance notes
    eligibility_notes: List[str] = Field(default_factory=list, description="Eligibility considerations")
    exclusion_warnings: List[str] = Field(default_factory=list, description="Important exclusions")


class ComparisonSummary(BaseModel):
    """High-level comparison summary"""
    total_policies_compared: int = Field(..., description="Number of policies compared")
    top_recommendation: str = Field(..., description="Top recommended insurer and product")
    coverage_range: Dict[str, int] = Field(..., description="Range of coverage options")
    price_indicators: Dict[str, Any] = Field(..., description="Price range indicators")
    takaful_options: int = Field(..., description="Number of takaful options")
    service_levels: Dict[str, int] = Field(..., description="Service level distribution")


class ComparisonMatrix(BaseModel):
    """Feature comparison matrix"""
    insurers: List[str] = Field(..., description="List of insurers")
    features: List[str] = Field(..., description="List of compared features")
    matrix: Dict[str, Dict[str, Any]] = Field(..., description="Feature comparison matrix")
    
    # Highlights
    best_coverage: Optional[str] = Field(None, description="Best overall coverage")
    best_service: Optional[str] = Field(None, description="Best service offering")
    best_value: Optional[str] = Field(None, description="Best value for money")
    most_comprehensive: Optional[str] = Field(None, description="Most comprehensive policy")


class ComparisonResult(BaseModel):
    """Complete comparison result"""
    # Request metadata
    session_id: str = Field(..., description="Comparison session ID")
    customer_name: str = Field(..., description="Customer name")
    comparison_date: datetime = Field(default_factory=datetime.now, description="Comparison timestamp")
    
    # Results
    recommendations: List[PolicyRecommendation] = Field(..., description="Ranked recommendations")
    summary: ComparisonSummary = Field(..., description="Comparison summary")
    matrix: ComparisonMatrix = Field(..., description="Feature comparison matrix")
    
    # Analysis
    market_insights: List[str] = Field(default_factory=list, description="Market insights")
    general_recommendations: List[str] = Field(default_factory=list, description="General advice")
    next_steps: List[str] = Field(default_factory=list, description="Recommended next steps")
    
    # Compliance
    data_sources: List[str] = Field(default_factory=list, description="Data source URLs")
    disclaimer: str = Field(default="", description="Legal disclaimer")
    compliance_notes: List[str] = Field(default_factory=list, description="Compliance considerations")
    
    # Processing metadata
    processing_time: Optional[float] = Field(None, description="Processing time in seconds")
    ai_model_used: Optional[str] = Field(None, description="AI model used for analysis")
    data_freshness: Dict[str, datetime] = Field(default_factory=dict, description="Data freshness per insurer")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }


class QuickCompareRequest(BaseModel):
    """Request model for quick policy comparison"""
    vehicle_type: str = Field(..., description="Type of vehicle (e.g., 'sedan', 'mpv', 'suv')")
    coverage_type: str = Field(..., description="Type of coverage (e.g., 'comprehensive', 'third_party')")
    max_price: Optional[float] = Field(None, description="Maximum price willing to pay")
    prefer_takaful: Optional[bool] = Field(None, description="Preference for Takaful products")
    
    @validator('vehicle_type')
    def validate_vehicle_type(cls, v):
        allowed_types = ['sedan', 'hatchback', 'mpv', 'suv', 'pickup', 'coupe', 'convertible', 'van', 'motorcycle']
        if v.lower() not in allowed_types:
            raise ValueError(f"Vehicle type must be one of: {allowed_types}")
        return v.lower()
    
    @validator('coverage_type')
    def validate_coverage_type(cls, v):
        allowed_types = ['comprehensive', 'third_party', 'third_party_fire_theft']
        if v.lower() not in allowed_types:
            raise ValueError(f"Coverage type must be one of: {allowed_types}")
        return v.lower()


class DetailedCompareRequest(BaseModel):
    """Request model for detailed policy comparison"""
    customer_input: Dict[str, Any] = Field(..., description="Complete customer profile and preferences")
    weights: Optional[Dict[str, float]] = Field(None, description="Custom weights for scoring algorithm")
    
    class Config:
        schema_extra = {
            "example": {
                "customer_input": {
                    "personal_info": {
                        "age": 30,
                        "gender": "male",
                        "marital_status": "married",
                        "occupation": "engineer",
                        "annual_income": 80000,
                        "driving_experience_years": 10
                    },
                    "vehicle_info": {
                        "make": "Honda",
                        "model": "Civic",
                        "year": 2020,
                        "engine_capacity": 1.5,
                        "vehicle_value": 85000,
                        "ncd_percentage": 25
                    },
                    "preferences": {
                        "coverage_preference": "comprehensive",
                        "price_range_max": 3000,
                        "prefers_takaful": False,
                        "preferred_insurers": ["Zurich Malaysia", "Etiqa"],
                        "important_features": ["roadside_assistance", "windscreen_cover"]
                    }
                },
                "weights": {
                    "coverage_weight": 0.30,
                    "service_weight": 0.25,
                    "takaful_weight": 0.10,
                    "pricing_weight": 0.25,
                    "eligibility_weight": 0.10
                }
            }
        }


class ComparisonSessionResponse(BaseModel):
    """Response model for comparison session operations"""
    status: str
    session_id: str
    message: str
    comparison_summary: Optional[Dict[str, Any]] = None
    
    class Config:
        schema_extra = {
            "example": {
                "status": "success",
                "session_id": "comp_123456789",
                "message": "Comparison completed successfully",
                "comparison_summary": {
                    "total_policies_compared": 8,
                    "top_recommendation": "Zurich Z-Driver",
                    "estimated_savings": 450.50,
                    "coverage_score": 8.5
                }
            }
        }


class ReportGenerationRequest(BaseModel):
    """Request model for custom report generation"""
    template_name: str = Field(default="default", description="Template to use for report")
    include_sections: List[str] = Field(default=["all"], description="Sections to include in report")
    custom_styling: Dict[str, Any] = Field(default_factory=dict, description="Custom styling options")
    
    @validator('include_sections')
    def validate_sections(cls, v):
        allowed_sections = [
            "all", "summary", "recommendations", "comparison_table", 
            "detailed_analysis", "pricing", "coverage", "terms"
        ]
        for section in v:
            if section not in allowed_sections:
                raise ValueError(f"Section '{section}' not allowed. Use: {allowed_sections}")
        return v


class EmailReportRequest(BaseModel):
    """Request model for email report delivery"""
    email_address: str = Field(..., description="Recipient email address")
    include_pdf: bool = Field(default=True, description="Include PDF attachment")
    include_summary: bool = Field(default=True, description="Include text summary")
    custom_message: Optional[str] = Field(None, description="Custom message to include")
    
    @validator('email_address')
    def validate_email(cls, v):
        if "@" not in v or "." not in v.split("@")[-1]:
            raise ValueError("Invalid email address format")
        return v.lower()


class ApiResponse(BaseModel):
    """Generic API response model"""
    status: str
    message: str
    data: Optional[Dict[str, Any]] = None
    errors: Optional[List[str]] = None
    timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        schema_extra = {
            "example": {
                "status": "success",
                "message": "Operation completed successfully",
                "data": {"result": "example_data"},
                "errors": None,
                "timestamp": "2024-01-15T10:30:00Z"
            }
        }


class PDFReportRequest(BaseModel):
    """Request for PDF report generation"""
    session_id: str = Field(..., description="Comparison session ID")
    include_detailed_matrix: bool = Field(default=True, description="Include detailed comparison matrix")
    include_policy_wordings: bool = Field(default=False, description="Include policy wording references")
    custom_notes: Optional[str] = Field(None, description="Custom notes to include")
    branding: Optional[Dict[str, str]] = Field(None, description="Custom branding options")


class PDFReportResponse(BaseModel):
    """Response for PDF report generation"""
    report_id: str = Field(..., description="Generated report ID")
    pdf_url: Optional[str] = Field(None, description="PDF download URL")
    pdf_path: Optional[str] = Field(None, description="PDF file path")
    generated_at: datetime = Field(default_factory=datetime.now, description="Generation timestamp")
    expires_at: Optional[datetime] = Field(None, description="URL expiration time")
    file_size: Optional[int] = Field(None, description="PDF file size in bytes")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }
