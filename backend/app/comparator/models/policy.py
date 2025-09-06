"""
Policy data models for normalized insurance policy representation
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator
from datetime import datetime
from enum import Enum


class CoverageType(str, Enum):
    """Types of motor insurance coverage"""
    COMPREHENSIVE = "Comprehensive"
    TPFT = "Third Party, Fire & Theft"
    THIRD_PARTY = "Third Party"


class ValuationMethod(str, Enum):
    """Vehicle valuation methods"""
    AGREED_VALUE = "Agreed Value"
    MARKET_VALUE = "Market Value"


class Eligibility(BaseModel):
    """Vehicle and driver eligibility requirements"""
    min_vehicle_age: Optional[int] = Field(None, description="Minimum vehicle age in years")
    max_vehicle_age: Optional[int] = Field(None, description="Maximum vehicle age in years")
    min_driver_age: Optional[int] = Field(None, description="Minimum driver age")
    max_driver_age: Optional[int] = Field(None, description="Maximum driver age")
    min_license_years: Optional[int] = Field(None, description="Minimum years holding license")
    excluded_vehicle_types: List[str] = Field(default_factory=list, description="Excluded vehicle categories")
    geographic_restrictions: List[str] = Field(default_factory=list, description="Geographic limitations")


class IncludedCover(BaseModel):
    """Standard coverage inclusions"""
    flood: bool = Field(default=False, description="Flood damage coverage")
    theft: bool = Field(default=False, description="Theft coverage")
    riot_strike: bool = Field(default=False, description="Riot and strike coverage")
    windscreen: bool = Field(default=False, description="Windscreen coverage")
    personal_accident: bool = Field(default=False, description="Personal accident coverage")
    accessories: bool = Field(default=False, description="Accessories coverage")
    natural_disaster: bool = Field(default=False, description="Natural disaster coverage")
    ehailing_coverage: bool = Field(default=False, description="E-hailing commercial use coverage")
    passenger_liability: bool = Field(default=False, description="Passenger liability coverage")
    legal_liability: bool = Field(default=False, description="Legal liability to passengers")


class AddOns(BaseModel):
    """Optional add-on coverages"""
    ncd_protection: Optional[Dict[str, Any]] = Field(None, description="NCD protection details")
    key_replacement: Optional[Dict[str, Any]] = Field(None, description="Key replacement coverage")
    courtesy_car: Optional[Dict[str, Any]] = Field(None, description="Courtesy car provision")
    towing_service: Optional[Dict[str, Any]] = Field(None, description="Towing service details")
    loss_of_use: Optional[Dict[str, Any]] = Field(None, description="Loss of use compensation")
    hospital_cash: Optional[Dict[str, Any]] = Field(None, description="Hospital cash benefit")
    betterment_waiver: Optional[Dict[str, Any]] = Field(None, description="Betterment waiver coverage")
    unnamed_driver: Optional[Dict[str, Any]] = Field(None, description="Unnamed driver extension")


class Services(BaseModel):
    """Service level offerings"""
    roadside_assist_24_7: bool = Field(default=False, description="24/7 roadside assistance")
    roadside_assist_sla: Optional[str] = Field(None, description="Response time SLA")
    towing_limit: Optional[str] = Field(None, description="Towing distance/amount limit")
    claim_fast_track: bool = Field(default=False, description="Fast track claims process")
    fast_track_threshold: Optional[str] = Field(None, description="Fast track claim amount threshold")
    panel_workshop_count: Optional[int] = Field(None, description="Number of panel workshops")
    digital_claims: bool = Field(default=False, description="Digital claims submission")
    mobile_app: bool = Field(default=False, description="Mobile app availability")
    online_portal: bool = Field(default=False, description="Online customer portal")


class PricingNotes(BaseModel):
    """Pricing and incentive information"""
    rebates: List[str] = Field(default_factory=list, description="Available rebates")
    cashback: List[str] = Field(default_factory=list, description="Cashback offers")
    bundling_discounts: List[str] = Field(default_factory=list, description="Bundle discounts")
    loyalty_benefits: List[str] = Field(default_factory=list, description="Loyalty program benefits")
    promotional_offers: List[str] = Field(default_factory=list, description="Current promotions")


class PolicyRecord(BaseModel):
    """Complete normalized policy record"""
    # Basic Information
    id: Optional[str] = Field(None, description="Database ID")
    insurer: str = Field(..., description="Insurance company name")
    product_name: str = Field(..., description="Product name")
    is_takaful: bool = Field(default=False, description="Whether this is a takaful product")
    coverage_type: CoverageType = Field(..., description="Type of coverage")
    valuation_method: Optional[ValuationMethod] = Field(None, description="Vehicle valuation method")
    
    # Requirements and Eligibility
    eligibility: Eligibility = Field(default_factory=Eligibility, description="Eligibility criteria")
    
    # Coverage Details
    included_cover: IncludedCover = Field(default_factory=IncludedCover, description="Included coverages")
    addons: AddOns = Field(default_factory=AddOns, description="Optional add-ons")
    services: Services = Field(default_factory=Services, description="Service offerings")
    
    # Commercial Information
    pricing_notes: PricingNotes = Field(default_factory=PricingNotes, description="Pricing information")
    exclusions: List[str] = Field(default_factory=list, description="Policy exclusions")
    
    # Metadata
    source_urls: List[str] = Field(default_factory=list, description="Source URLs")
    last_checked: Optional[datetime] = Field(None, description="Last data update")
    created_at: Optional[datetime] = Field(None, description="Record creation time")
    updated_at: Optional[datetime] = Field(None, description="Last record update")
    
    @validator('insurer')
    def validate_insurer(cls, v):
        valid_insurers = [
            'Zurich Malaysia', 'Etiqa', 'Allianz General Insurance Malaysia',
            'AXA Affin General', 'Generali Malaysia', 'Liberty Insurance',
            'AmGeneral', 'Takaful Ikhlas', 'Berjaya Sompo', 'Tokio Marine',
            'Great Eastern General'
        ]
        if v not in valid_insurers:
            # Allow for variations, but log for review
            pass
        return v
    
    class Config:
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }


class PolicySummary(BaseModel):
    """Lightweight policy summary for listings"""
    id: str
    insurer: str
    product_name: str
    is_takaful: bool
    coverage_type: CoverageType
    last_checked: Optional[datetime]
    
    class Config:
        use_enum_values = True


class PersonalInfo(BaseModel):
    """Personal information for customer"""
    age: Optional[int] = Field(None, description="Customer age")
    gender: Optional[str] = Field(None, description="Customer gender")
    marital_status: Optional[str] = Field(None, description="Marital status")
    occupation: Optional[str] = Field(None, description="Occupation")
    annual_income: Optional[float] = Field(None, description="Annual income in RM")
    driving_experience_years: Optional[int] = Field(None, description="Years of driving experience")
    
    @validator('gender')
    def validate_gender(cls, v):
        if v and v.lower() not in ['male', 'female']:
            raise ValueError("Gender must be 'male' or 'female'")
        return v.lower() if v else v


class VehicleInfo(BaseModel):
    """Vehicle information for insurance"""
    make: Optional[str] = Field(None, description="Vehicle make (Honda, Toyota, etc.)")
    model: Optional[str] = Field(None, description="Vehicle model")
    year: Optional[int] = Field(None, description="Vehicle year")
    engine_capacity: Optional[float] = Field(None, description="Engine capacity in liters")
    vehicle_value: Optional[float] = Field(None, description="Current vehicle value in RM")
    vehicle_age: Optional[int] = Field(None, description="Vehicle age in years")
    ncd_percentage: Optional[int] = Field(None, description="No Claim Discount percentage")
    vehicle_type: Optional[str] = Field(None, description="Vehicle type (sedan, SUV, etc.)")
    
    @validator('ncd_percentage')
    def validate_ncd(cls, v):
        if v is not None and (v < 0 or v > 55):
            raise ValueError("NCD percentage must be between 0 and 55")
        return v


class CustomerPreferences(BaseModel):
    """Customer preferences and requirements"""
    coverage_preference: str = Field(..., description="Preferred coverage type")
    price_range_min: Optional[float] = Field(None, description="Minimum acceptable price")
    price_range_max: Optional[float] = Field(None, description="Maximum acceptable price")
    prefers_takaful: bool = Field(default=False, description="Prefers Takaful products")
    preferred_insurers: List[str] = Field(default_factory=list, description="Preferred insurance companies")
    important_features: List[str] = Field(default_factory=list, description="Important policy features")
    
    @validator('coverage_preference')
    def validate_coverage_preference(cls, v):
        valid_types = ['comprehensive', 'third_party', 'third_party_fire_theft']
        if v.lower() not in valid_types:
            raise ValueError(f"Coverage preference must be one of: {valid_types}")
        return v.lower()


class CustomerInput(BaseModel):
    """Complete customer input for policy comparison"""
    personal_info: Optional[PersonalInfo] = Field(None, description="Personal information")
    vehicle_info: Optional[VehicleInfo] = Field(None, description="Vehicle information") 
    preferences: Optional[CustomerPreferences] = Field(None, description="Customer preferences")
    
    # Quick comparison fields
    vehicle_type: Optional[str] = Field(None, description="Quick vehicle type selection")
    coverage_preference: Optional[str] = Field(None, description="Quick coverage preference")
    price_range_max: Optional[float] = Field(None, description="Quick max price")
    prefers_takaful: Optional[bool] = Field(None, description="Quick Takaful preference")
