from pydantic import BaseModel, Field
from typing import List, Optional

class ClaimPredictionRequest(BaseModel):
    incidentType: str = Field(..., description="Type of incident")
    timeOfDay: str = Field(..., description="Time of day when the incident occurred")
    roadConditions: str = Field(..., description="Road conditions at the time of the incident")
    weatherConditions: str = Field(..., description="Weather conditions at the time of the incident")
    injuries: str = Field(..., description="Whether there were any injuries")
    vehicleDamage: str = Field(..., description="Extent of vehicle damage")
    thirdPartyVehicle: str = Field(..., description="Whether a third-party vehicle was involved")
    witnesses: str = Field(..., description="Whether there were any witnesses")
    policeReport: str = Field(..., description="Whether a police report was filed")
    description: str = Field(..., description="A brief description of the incident")

class ClaimPredictionResponse(BaseModel):
    prediction: int = Field(..., description="Predicted success rate of the claim (0-100)")
    confidence: float = Field(..., description="Confidence level of the prediction (0.0-1.0)")
    confidence_score: float = Field(..., description="Final confidence score calculated as prediction * confidence")
    key_factors: List[str] = Field(..., description="Key factors influencing the prediction")
    ai_insights: Optional[str] = Field(None, description="AI-generated insights based on the policy document and incident description")
