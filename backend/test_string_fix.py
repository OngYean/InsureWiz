#!/usr/bin/env python3
"""
Test the string method error fix directly
"""
import sys
import os

# Add the backend directory to Python path
sys.path.append('/home/ongyn/Documents/InsureWiz/backend')

from app.ml.predict import run_prediction
import io

def test_string_error_fix():
    """Test that the string method error is fixed"""
    
    # Create test data with problematic types (integers instead of strings)
    form_data = {
        'incident_description': 123,  # Integer that was causing .lower() error
        'driver_age': 30,
        'vehicle_age': 5,
        'engine_capacity': 2000,
        'market_value': 25000,
        'policeReport': 1,      # Integer instead of "yes"/"no"
        'witnesses': 0,         # Integer instead of "yes"/"no"
        'injuries': 1,          # Integer instead of "yes"/"no"
        'weatherConditions': 2, # Integer instead of string
        'trafficViolation': 0   # Integer instead of "yes"/"no"
    }
    
    # Create empty policy document
    policy_doc = io.BytesIO(b"")
    
    # Create empty evidence files
    evidence_files = [io.BytesIO(b"test evidence")]
    
    try:
        result = run_prediction(form_data, policy_doc, evidence_files)
        print("✅ SUCCESS: No string method errors!")
        print(f"Prediction: {result['prediction']}")
        print(f"Confidence: {result['confidence']}")
        print(f"Confidence Score: {result['confidence_score']}")
        print(f"Key Factors: {len(result['key_factors'])} factors")
        print(f"AI Insights: {result['ai_insights'][:100]}...")
        return True
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    print("Testing string method error fix...")
    test_string_error_fix()
