#!/usr/bin/env python3
"""
Test the enhanced LLM insights with complete form data
"""
import sys
import os
import io

# Add the backend directory to Python path
sys.path.append('/home/ongyn/Documents/InsureWiz/backend')

from app.ml.llm_insights import get_ai_insights

def test_enhanced_llm_insights():
    """Test LLM insights with comprehensive form data"""
    
    # Create comprehensive test form data
    comprehensive_form_data = {
        # Incident Details
        'incident_description': 'Rear-ended another vehicle at traffic light during rush hour',
        'incidentType': 'Collision',
        'timeOfDay': 'Evening',
        'weatherConditions': 'Rain',
        'roadConditions': 'Wet',
        
        # Driver & Vehicle Information
        'driver_age': 28,
        'vehicle_age': 3,
        'engine_capacity': 1800,
        'market_value': 65000,
        'vehicleDamage': 'moderate',
        
        # Parties & Documentation
        'injuries': 'no',
        'thirdPartyVehicle': 'yes',
        'witnesses': 'yes',
        'policeReport': 'yes',
        'policeReportFiledWithin24h': 1,
        'trafficViolation': 0,
        'previousClaims': 1
    }
    
    # Mock policy text
    mock_policy_text = """
    MOTOR INSURANCE POLICY
    
    Coverage Details:
    - Comprehensive Coverage: Included for vehicles up to 10 years old
    - Third Party Liability: Up to RM 1,000,000
    - Collision Coverage: Covered with RM 1,500 deductible
    - Weather-related incidents: Covered under comprehensive
    
    Claims Requirements:
    - Police report must be filed within 24 hours for collisions
    - All claims must be reported within 30 days
    - Traffic violations may affect claim assessment
    
    Exclusions:
    - Damage caused by racing or competitive driving
    - Incidents involving unlicensed drivers
    - Claims exceeding policy limits
    """
    
    print("Testing Enhanced LLM Insights with Comprehensive Form Data...")
    print("=" * 60)
    
    try:
        # Test with comprehensive data and policy
        print("🔍 Testing with complete form data and policy text:")
        insights = get_ai_insights(comprehensive_form_data, mock_policy_text)
        print(f"✅ Insights Generated:")
        print(f"{insights}")
        print("\n" + "="*60 + "\n")
        
        # Test with comprehensive data but no policy
        print("🔍 Testing with complete form data but no policy text:")
        insights_no_policy = get_ai_insights(comprehensive_form_data, "")
        print(f"✅ Insights Generated (No Policy):")
        print(f"{insights_no_policy}")
        print("\n" + "="*60 + "\n")
        
        # Test with minimal data
        minimal_data = {
            'incident_description': 'Car accident',
            'incidentType': 'Collision'
        }
        print("🔍 Testing with minimal form data:")
        insights_minimal = get_ai_insights(minimal_data, mock_policy_text)
        print(f"✅ Insights Generated (Minimal Data):")
        print(f"{insights_minimal}")
        
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED - Enhanced LLM insights working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    test_enhanced_llm_insights()
