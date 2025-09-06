"""
Simple scoring utilities without circular imports
"""

from pydantic import BaseModel, Field
from typing import Dict, Any


class ScoreWeights(BaseModel):
    """Configurable weights for policy scoring"""
    coverage_weight: float = Field(default=0.25, description="Coverage breadth weight")
    service_weight: float = Field(default=0.20, description="Service quality weight") 
    takaful_weight: float = Field(default=0.15, description="Takaful preference weight")
    pricing_weight: float = Field(default=0.25, description="Pricing attractiveness weight")
    eligibility_weight: float = Field(default=0.15, description="Eligibility match weight")


def calculate_policy_score(policy, weights: ScoreWeights = None) -> float:
    """Calculate a simple policy score"""
    if weights is None:
        weights = ScoreWeights()
    
    # Simple scoring based on available data
    score = 0.0
    
    # Coverage score (0-100)
    coverage_score = 50.0  # Base score
    if hasattr(policy, 'coverage_details') and policy.coverage_details:
        coverage_count = len([v for v in policy.coverage_details.values() if v])
        coverage_score = min(100, 40 + (coverage_count * 10))
    
    # Pricing score (0-100) 
    pricing_score = 50.0  # Base score
    if hasattr(policy, 'pricing') and policy.pricing and 'base_premium' in policy.pricing:
        premium = policy.pricing['base_premium']
        # Score based on price range (lower is better)
        if premium < 2000:
            pricing_score = 90
        elif premium < 3000:
            pricing_score = 75
        elif premium < 4000:
            pricing_score = 60
        else:
            pricing_score = 40
    
    # Service score (default)
    service_score = 70.0
    
    # Takaful score (matches preference)
    takaful_score = 50.0
    if hasattr(policy, 'is_takaful'):
        takaful_score = 100 if policy.is_takaful else 50
    
    # Eligibility score (default)
    eligibility_score = 80.0
    
    # Calculate weighted total
    total_score = (
        coverage_score * weights.coverage_weight +
        service_score * weights.service_weight +
        takaful_score * weights.takaful_weight +
        pricing_score * weights.pricing_weight +
        eligibility_score * weights.eligibility_weight
    )
    
    return round(total_score, 1)
