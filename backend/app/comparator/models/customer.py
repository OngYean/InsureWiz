"""
Customer input models for insurance comparison requests
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator
from enum import Enum


class VehicleType(str, Enum):
    """Types of vehicles"""
    SEDAN = "Sedan"
    SUV = "SUV"
    HATCHBACK = "Hatchback"
    MPV = "MPV"
    COUPE = "Coupe"
    CONVERTIBLE = "Convertible"
    PICKUP = "Pickup"
    MOTORCYCLE = "Motorcycle"


class UsageType(str, Enum):
    """Vehicle usage types"""
    PERSONAL = "Personal"
    COMMERCIAL = "Commercial"
    EHAILING = "E-hailing"
    BUSINESS = "Business"


class State(str, Enum):
    """Malaysian states"""
    JOHOR = "Johor"
    KEDAH = "Kedah"
    KELANTAN = "Kelantan"
    MALACCA = "Malacca"
    NEGERI_SEMBILAN = "Negeri Sembilan"
    PAHANG = "Pahang"
    PENANG = "Penang"
    PERAK = "Perak"
    PERLIS = "Perlis"
    SABAH = "Sabah"
    SARAWAK = "Sarawak"
    SELANGOR = "Selangor"
    TERENGGANU = "Terengganu"
    KUALA_LUMPUR = "Kuala Lumpur"
    LABUAN = "Labuan"
    PUTRAJAYA = "Putrajaya"


class CoveragePriority(str, Enum):
    """Customer coverage priorities"""
    BASIC = "Basic"
    STANDARD = "Standard"
    COMPREHENSIVE = "Comprehensive"
    PREMIUM = "Premium"


class Vehicle(BaseModel):
    """Vehicle information"""
    make: str = Field(..., description="Vehicle manufacturer")
    model: str = Field(..., description="Vehicle model")
    year: int = Field(..., description="Vehicle year", ge=1980, le=2030)
    vehicle_type: VehicleType = Field(..., description="Type of vehicle")
    engine_capacity: Optional[float] = Field(None, description="Engine capacity in CC")
    estimated_value: Optional[float] = Field(None, description="Estimated vehicle value in RM")
    usage_type: UsageType = Field(default=UsageType.PERSONAL, description="Vehicle usage")
    
    @validator('year')
    def validate_year(cls, v):
        from datetime import datetime
        current_year = datetime.now().year
        if v > current_year + 1:
            raise ValueError(f"Vehicle year cannot be more than {current_year + 1}")
        return v


class Driver(BaseModel):
    """Primary driver information"""
    age: int = Field(..., description="Driver age", ge=18, le=99)
    license_years: int = Field(..., description="Years holding license", ge=0)
    gender: Optional[str] = Field(None, description="Driver gender")
    marital_status: Optional[str] = Field(None, description="Marital status")
    occupation: Optional[str] = Field(None, description="Occupation")
    
    @validator('license_years')
    def validate_license_years(cls, v, values):
        if 'age' in values and v > values['age'] - 16:
            raise ValueError("License years cannot exceed possible driving experience")
        return v


class CustomerPreferences(BaseModel):
    """Customer preferences and priorities"""
    takaful_preference: bool = Field(default=False, description="Prefer takaful products")
    coverage_priority: CoveragePriority = Field(default=CoveragePriority.STANDARD, description="Coverage level preference")
    budget_range: Optional[Dict[str, float]] = Field(None, description="Budget range (min/max)")
    important_features: List[str] = Field(default_factory=list, description="Important features/add-ons")
    service_priorities: List[str] = Field(default_factory=list, description="Service priorities")
    preferred_insurers: List[str] = Field(default_factory=list, description="Preferred insurance companies")
    excluded_insurers: List[str] = Field(default_factory=list, description="Insurers to exclude")


class CustomerInput(BaseModel):
    """Complete customer input for comparison"""
    # Personal Information
    name: str = Field(..., description="Customer name")
    email: Optional[str] = Field(None, description="Customer email")
    phone: Optional[str] = Field(None, description="Customer phone")
    state: State = Field(..., description="Customer state")
    
    # Vehicle and Driver
    vehicle: Vehicle = Field(..., description="Vehicle information")
    driver: Driver = Field(..., description="Primary driver information")
    
    # Preferences
    preferences: CustomerPreferences = Field(default_factory=CustomerPreferences, description="Customer preferences")
    
    # Compliance
    consent_data_processing: bool = Field(default=False, description="Consent for data processing")
    consent_marketing: bool = Field(default=False, description="Consent for marketing communications")
    
    @validator('consent_data_processing')
    def validate_consent(cls, v):
        if not v:
            raise ValueError("Data processing consent is required for comparison")
        return v
    
    class Config:
        use_enum_values = True


class ComparisonRequest(BaseModel):
    """Request for policy comparison"""
    customer: CustomerInput = Field(..., description="Customer information")
    max_results: int = Field(default=10, description="Maximum number of results", ge=1, le=50)
    include_expired: bool = Field(default=False, description="Include expired policies")
    force_refresh: bool = Field(default=False, description="Force refresh of policy data")
    
    class Config:
        use_enum_values = True
