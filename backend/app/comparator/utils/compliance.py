"""
Compliance utilities for BNM and PDPA requirements
"""

import logging
from typing import Dict, Any, List
from datetime import datetime, timedelta
import json

logger = logging.getLogger(__name__)

class ComplianceManager:
    """Manager for regulatory compliance requirements"""
    
    def __init__(self):
        self.data_retention_days = 365 * 7  # 7 years for financial services
        self.consent_validity_days = 365     # 1 year for marketing consent
    
    def log_data_processing(self, customer_info: Dict[str, Any], purpose: str, legal_basis: str = "consent") -> str:
        """Log data processing activity for PDPA compliance"""
        processing_record = {
            "timestamp": datetime.now().isoformat(),
            "customer_id": customer_info.get("email") or customer_info.get("phone"),
            "data_types": list(customer_info.keys()),
            "processing_purpose": purpose,
            "legal_basis": legal_basis,
            "retention_until": (datetime.now() + timedelta(days=self.data_retention_days)).isoformat()
        }
        
        # In production, this would be stored in a secure audit log
        logger.info(f"PDPA Log: {json.dumps(processing_record)}")
        
        return processing_record["timestamp"]
    
    def validate_consent(self, consent_data: Dict[str, Any]) -> Dict[str, bool]:
        """Validate customer consent for various processing purposes"""
        validation_result = {
            "data_processing_valid": False,
            "marketing_valid": False,
            "storage_valid": False
        }
        
        # Check data processing consent (required)
        if consent_data.get("consent_data_processing"):
            validation_result["data_processing_valid"] = True
        
        # Check marketing consent (optional)
        if consent_data.get("consent_marketing"):
            # Check if consent is still valid (within validity period)
            consent_date = datetime.fromisoformat(consent_data.get("consent_date", datetime.now().isoformat()))
            if datetime.now() - consent_date < timedelta(days=self.consent_validity_days):
                validation_result["marketing_valid"] = True
        
        # Data storage consent (implied with processing consent)
        validation_result["storage_valid"] = validation_result["data_processing_valid"]
        
        return validation_result
    
    def get_pdpa_notice(self) -> str:
        """Get PDPA privacy notice text"""
        return """
PERSONAL DATA PROTECTION NOTICE

InsureWiz collects and processes your personal data for the following purposes:
1. Insurance policy comparison and recommendation
2. Customer service and support
3. Regulatory compliance and record keeping

Your data will be shared with:
- Insurance companies for quotation purposes (with your consent)
- Regulatory authorities as required by law

Your rights:
- Access your personal data
- Correct inaccurate data
- Withdraw consent (may limit services)
- Lodge complaints with PDPA authorities

Data retention: 7 years from last interaction or as required by law.

By proceeding, you consent to the collection and processing of your personal data as described.
"""
    
    def log_recommendation_rationale(self, session_id: str, customer_data: Dict[str, Any], recommendations: List[Dict[str, Any]]) -> str:
        """Log recommendation rationale for BNM compliance"""
        rationale_record = {
            "session_id": session_id,
            "timestamp": datetime.now().isoformat(),
            "customer_profile": {
                "age": customer_data.get("driver", {}).get("age"),
                "vehicle_type": customer_data.get("vehicle", {}).get("vehicle_type"),
                "state": customer_data.get("state"),
                "coverage_priority": customer_data.get("preferences", {}).get("coverage_priority"),
                "takaful_preference": customer_data.get("preferences", {}).get("takaful_preference")
            },
            "methodology": "Weighted scoring system with AI analysis",
            "factors_considered": [
                "Coverage breadth (25%)",
                "Service quality (20%)", 
                "Religious preference match (15%)",
                "Pricing attractiveness (25%)",
                "Eligibility match (15%)"
            ],
            "recommendations": [
                {
                    "rank": rec.get("rank"),
                    "insurer": rec.get("policy", {}).get("insurer"),
                    "product": rec.get("policy", {}).get("product_name"),
                    "score": rec.get("score", {}).get("total_score"),
                    "rationale": rec.get("strengths", [])
                }
                for rec in recommendations[:3]  # Top 3 only
            ],
            "data_sources": "Official insurer websites",
            "disclaimers": [
                "Subject to underwriting approval",
                "Prices may vary based on individual circumstances",
                "Customer advised to verify details with insurers"
            ]
        }
        
        # In production, this would be stored in a secure audit log
        logger.info(f"BNM Compliance Log: {json.dumps(rationale_record)}")
        
        return rationale_record["timestamp"]
    
    def get_bnm_disclaimer(self) -> str:
        """Get BNM-compliant disclaimer text"""
        return """
IMPORTANT DISCLAIMER

This comparison service is provided for informational purposes only. All recommendations are based on:
- Publicly available information from insurers' official sources
- Customer-disclosed information and preferences
- Standardized comparison methodology

Key Considerations:
- All policies are subject to underwriting approval
- Actual premiums may vary based on individual risk assessment
- Coverage terms and conditions may differ from summaries presented
- Customers are advised to read full policy wordings before purchasing

This service complies with Bank Negara Malaysia guidelines on the professionalism of insurance agents and intermediaries. All processing activities are conducted in accordance with the Personal Data Protection Act 2010.

For complaints or queries, please contact:
- Bank Negara Malaysia (BNM): 1-300-88-5465
- Personal Data Protection Department: 03-8911 7000
"""

class AuditTrail:
    """Audit trail for compliance tracking"""
    
    def __init__(self):
        self.activities = []
    
    def log_activity(self, activity_type: str, details: Dict[str, Any], session_id: str = None):
        """Log an activity for audit purposes"""
        activity = {
            "timestamp": datetime.now().isoformat(),
            "activity_type": activity_type,
            "session_id": session_id,
            "details": details,
            "ip_address": details.get("ip_address", "unknown"),
            "user_agent": details.get("user_agent", "unknown")
        }
        
        self.activities.append(activity)
        logger.info(f"Audit: {activity_type} - Session: {session_id}")
    
    def get_session_trail(self, session_id: str) -> List[Dict[str, Any]]:
        """Get audit trail for a specific session"""
        return [activity for activity in self.activities if activity.get("session_id") == session_id]
    
    def cleanup_old_records(self, days_to_keep: int = 2555):  # 7 years
        """Clean up old audit records (for data retention compliance)"""
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        
        before_count = len(self.activities)
        self.activities = [
            activity for activity in self.activities
            if datetime.fromisoformat(activity["timestamp"]) > cutoff_date
        ]
        after_count = len(self.activities)
        
        logger.info(f"Audit cleanup: Removed {before_count - after_count} old records")

# Global instances
compliance_manager = ComplianceManager()
audit_trail = AuditTrail()
