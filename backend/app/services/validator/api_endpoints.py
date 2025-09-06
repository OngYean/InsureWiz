"""
API endpoints for vehicle validation and suggestions
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Optional
from pydantic import BaseModel

from .data_loader import vehicle_data_loader
from .suggestion_engine import suggestion_engine
from .validation_service import malaysian_validator
from .langchain_validation_service import vehicle_validation_agent


router = APIRouter(prefix="/api/validator", tags=["validator"])


class ValidationRequest(BaseModel):
    ic: Optional[str] = None
    plate_number: Optional[str] = None


class VehicleValidationRequest(BaseModel):
    year: int
    brand: str
    model: str
    color: str
    owner_ic: str
    plate_number: str


class SuggestionResponse(BaseModel):
    primary: Optional[str]
    suggestions: List[str]
    completion: str


class YearDataResponse(BaseModel):
    year: int
    brands: List[str]
    models: Dict[str, List[str]]
    colors: Dict[str, Dict[str, List[str]]]


@router.get("/years", response_model=List[int])
async def get_available_years():
    """Get all available years for vehicle data"""
    try:
        years = vehicle_data_loader.get_available_years()
        return years
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading years: {str(e)}")


@router.get("/year-data/{year}", response_model=YearDataResponse)
async def get_year_data(year: int):
    """Get all brands, models, and colors for a specific year (for frontend caching)"""
    try:
        # Validate year
        available_years = vehicle_data_loader.get_available_years()
        year_validation = malaysian_validator.validate_year(year, available_years)
        if not year_validation['valid']:
            raise HTTPException(status_code=400, detail=year_validation['error'])
        
        # Load data for the year
        brands = vehicle_data_loader.get_brands(year)
        
        # Build complete dataset
        models = {}
        colors = {}
        
        for brand in brands:
            brand_models = vehicle_data_loader.get_models_for_brand(year, brand)
            models[brand] = brand_models
            
            brand_colors = {}
            for model in brand_models:
                model_colors = vehicle_data_loader.get_colors_for_model(year, brand, model)
                brand_colors[model] = model_colors
            colors[brand] = brand_colors
        
        return YearDataResponse(
            year=year,
            brands=brands,
            models=models,
            colors=colors
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading year data: {str(e)}")


@router.get("/brands", response_model=SuggestionResponse)
async def get_brand_suggestions(
    year: int = Query(..., description="Registration year"),
    query: str = Query("", description="Search query for brand")
):
    """Get brand suggestions for a specific year"""
    try:
        # Validate year
        available_years = vehicle_data_loader.get_available_years()
        year_validation = malaysian_validator.validate_year(year, available_years)
        if not year_validation['valid']:
            raise HTTPException(status_code=400, detail=year_validation['error'])
        
        # Get brands for the year
        brands = vehicle_data_loader.get_brands(year)
        
        # Get suggestions
        if query:
            suggestions = suggestion_engine.get_brand_suggestions(query, brands)
        else:
            # Return all brands if no query
            suggestions = {
                'primary': None,
                'suggestions': brands[:5],  # Limit to first 5
                'completion': ''
            }
        
        return SuggestionResponse(**suggestions)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting brand suggestions: {str(e)}")


@router.get("/models", response_model=SuggestionResponse)
async def get_model_suggestions(
    year: int = Query(..., description="Registration year"),
    brand: str = Query(..., description="Vehicle brand/maker"),
    query: str = Query("", description="Search query for model")
):
    """Get model suggestions for a specific brand and year"""
    try:
        # Validate year
        available_years = vehicle_data_loader.get_available_years()
        year_validation = malaysian_validator.validate_year(year, available_years)
        if not year_validation['valid']:
            raise HTTPException(status_code=400, detail=year_validation['error'])
        
        # Get models for the brand (case-insensitive)
        brands = vehicle_data_loader.get_brands(year)
        
        # Find exact brand match (case-insensitive)
        brand_exact = brand
        for b in brands:
            if b.lower() == brand.lower():
                brand_exact = b
                break
        
        models = vehicle_data_loader.get_models_for_brand(year, brand_exact)
        
        if not models:
            return SuggestionResponse(primary=None, suggestions=[], completion="")
        
        # Get suggestions
        if query:
            suggestions = suggestion_engine.get_model_suggestions(query, models)
        else:
            # Return all models if no query
            suggestions = {
                'primary': None,
                'suggestions': models[:5],  # Limit to first 5
                'completion': ''
            }
        
        return SuggestionResponse(**suggestions)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting model suggestions: {str(e)}")


@router.get("/colors", response_model=SuggestionResponse)
async def get_color_suggestions(
    year: int = Query(..., description="Registration year"),
    brand: str = Query(..., description="Vehicle brand/maker"),
    model: str = Query(..., description="Vehicle model"),
    query: str = Query("", description="Search query for color")
):
    """Get color suggestions for a specific brand, model and year"""
    try:
        # Validate year
        available_years = vehicle_data_loader.get_available_years()
        year_validation = malaysian_validator.validate_year(year, available_years)
        if not year_validation['valid']:
            raise HTTPException(status_code=400, detail=year_validation['error'])
        
        # Get colors for the brand and model (case-insensitive)
        brands = vehicle_data_loader.get_brands(year)
        models = []
        
        # Find exact brand match (case-insensitive)
        brand_exact = brand
        for b in brands:
            if b.lower() == brand.lower():
                brand_exact = b
                break
        
        if brand_exact:
            models = vehicle_data_loader.get_models_for_brand(year, brand_exact)
            
            # Find exact model match (case-insensitive)
            model_exact = model
            for m in models:
                if m.lower() == model.lower():
                    model_exact = m
                    break
            
            if model_exact:
                colors = vehicle_data_loader.get_colors_for_model(year, brand_exact, model_exact)
            else:
                colors = []
        else:
            colors = []
        
        if not colors:
            return SuggestionResponse(primary=None, suggestions=[], completion="")
        
        # Get suggestions
        if query:
            suggestions = suggestion_engine.get_color_suggestions(query, colors)
        else:
            # Return all colors if no query
            suggestions = {
                'primary': None,
                'suggestions': colors[:5],  # Limit to first 5
                'completion': ''
            }
        
        return SuggestionResponse(**suggestions)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting color suggestions: {str(e)}")


@router.post("/validate-vehicle")
async def validate_vehicle_comprehensive(request: VehicleValidationRequest):
    """Comprehensive vehicle validation using LangChain and Tavily"""
    try:
        # Convert request to dict
        vehicle_data = {
            "year": request.year,
            "brand": request.brand,
            "model": request.model,
            "color": request.color,
            "owner_ic": request.owner_ic,
            "plate_number": request.plate_number
        }
        
        # Validate formats first
        ic_validation = malaysian_validator.validate_ic(request.owner_ic)
        plate_validation = malaysian_validator.validate_plate_number(request.plate_number)
        
        if not ic_validation['valid']:
            raise HTTPException(status_code=400, detail=f"Invalid IC: {ic_validation['error']}")
        
        if not plate_validation['valid']:
            raise HTTPException(status_code=400, detail=f"Invalid plate number: {plate_validation['error']}")
        
        # Perform comprehensive validation
        validation_result = await vehicle_validation_agent.validate_vehicle(vehicle_data)
        
        return validation_result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error validating vehicle: {str(e)}")


@router.post("/validate-formats")
async def validate_formats(request: ValidationRequest):
    """Validate Malaysian IC and plate number formats"""
    try:
        result = {}
        
        if request.ic:
            result['ic'] = malaysian_validator.validate_ic(request.ic)
        
        if request.plate_number:
            result['plate_number'] = malaysian_validator.validate_plate_number(request.plate_number)
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error validating formats: {str(e)}")


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "vehicle-validator"}
