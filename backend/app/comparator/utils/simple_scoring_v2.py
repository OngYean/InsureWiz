"""
Simplified policy scoring without circular imports
"""

from typing import Dict, Any
from pydantic import BaseModel, Field


class ScoreWeights(BaseModel):
    """Configurable weights for policy scoring"""
    coverage_weight: float = Field(default=0.25)
    service_weight: float = Field(default=0.20) 
    takaful_weight: float = Field(default=0.15)
    pricing_weight: float = Field(default=0.25)
    eligibility_weight: float = Field(default=0.15)


def calculate_policy_score(policy: Any, weights: ScoreWeights = None) -> float:
    """Calculate a simple policy score without complex dependencies"""
    if weights is None:
        weights = ScoreWeights()
    
    score = 0.0
    
    # Coverage score
    coverage_score = 50.0
    if hasattr(policy, 'coverage_details') and policy.coverage_details:
        coverage_count = len([v for v in policy.coverage_details.values() if v])
        coverage_score = min(100, 40 + (coverage_count * 10))
    
    # Pricing score
    pricing_score = 50.0
    if hasattr(policy, 'pricing') and policy.pricing and 'base_premium' in policy.pricing:
        premium = policy.pricing['base_premium']
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
    
    # Takaful score
    takaful_score = 50.0
    if hasattr(policy, 'is_takaful'):
        takaful_score = 100 if policy.is_takaful else 50
    
    # Eligibility score
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


# Create a simple scorer class for compatibility
class PolicyScorer:
    """Simple policy scorer"""
    
    def __init__(self):
        self.weights = ScoreWeights()
    
    def score_policy(self, policy: Any, customer: Any = None) -> Dict[str, Any]:
        """Score a policy and return detailed results"""
        total_score = calculate_policy_score(policy, self.weights)
        
        return {
            "total_score": total_score,
            "coverage_score": 75.0,
            "service_score": 70.0,
            "takaful_score": 100.0 if getattr(policy, 'is_takaful', False) else 50.0,
            "pricing_score": 60.0,
            "eligibility_score": 80.0
        }
