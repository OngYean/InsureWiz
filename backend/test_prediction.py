#!/usr/bin/env python3

"""
Test script to debug the claim prediction pipeline
"""

import sys
import os
import io

# Add the backend directory to Python path
sys.path.append('/home/ongyn/Documents/InsureWiz/backend')

from app.ml.predict import run_prediction

def test_prediction():
    """Test the prediction pipeline with sample data"""
    
    # Sample form data with all required fields
    form_data = {
        "incident_description": "My car was hit by another vehicle in a parking lot",
        "driver_age": 25,
        "vehicle_age": 3,
        "engine_capacity": 1500,
        "market_value": 50000,
        # Additional required fields for the ML model
        "incidentType": "collision",
        "timeOfDay": "afternoon",
        "roadConditions": "dry",
        "weatherConditions": "clear",
        "injuries": "no",
        "thirdPartyVehicle": "yes",
        "witnesses": "yes",
        "policeReport": "yes",
        "policeReportFiledWithin24h": "yes",
        "trafficViolation": "no",
        "previousClaims": "no",
        "vehicleDamage": "moderate"
    }
    
    # Create dummy evidence files (empty bytes)
    evidence_files_bytes = [b"test image data"]
    
    # Create dummy policy document (simple text as bytes)
    policy_text = "Sample policy document text for testing"
    policy_document_io = io.BytesIO(policy_text.encode('utf-8'))
    
    print("Testing prediction pipeline...")
    print(f"Form data: {form_data}")
    print(f"Evidence files: {len(evidence_files_bytes)} files")
    print(f"Policy document size: {len(policy_text)} chars")
    
    try:
        result = run_prediction(form_data, evidence_files_bytes, policy_document_io)
        print("\n✅ Prediction successful!")
        print(f"Result: {result}")
        
    except Exception as e:
        print(f"\n❌ Prediction failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_prediction()
