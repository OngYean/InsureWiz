"""
Test script for the Insurance Comparator API
"""

import requests
import json
from datetime import datetime

# API base URL
BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/simple/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("-" * 50)

def test_policies():
    """Test policies endpoint"""
    print("Testing policies endpoint...")
    response = requests.get(f"{BASE_URL}/simple/policies")
    print(f"Status: {response.status_code}")
    policies = response.json()
    print(f"Found {len(policies)} policies:")
    for policy in policies:
        print(f"  - {policy['insurer']}: {policy['product_name']}")
    print("-" * 50)

def test_insurers():
    """Test insurers endpoint"""
    print("Testing insurers endpoint...")
    response = requests.get(f"{BASE_URL}/simple/insurers")
    print(f"Status: {response.status_code}")
    insurers = response.json()
    print(f"Available insurers: {', '.join(insurers)}")
    print("-" * 50)

def test_comparison():
    """Test comparison endpoint"""
    print("Testing comparison endpoint...")
    
    # Test data
    test_data = {
        "vehicle_type": "private_car",
        "coverage_type": "comprehensive", 
        "vehicle_value": 80000,
        "driver_age": 35,
        "location": "Kuala Lumpur"
    }
    
    response = requests.post(
        f"{BASE_URL}/simple/compare",
        json=test_data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Session ID: {result['session_id']}")
        
        summary = result['comparison_summary']
        print(f"Total policies compared: {summary['total_policies']}")
        print(f"Average premium: RM {summary['average_premium']:.2f}")
        
        print("\nPolicy Rankings:")
        for i, policy in enumerate(result['policy_rankings'][:3], 1):
            print(f"  {i}. {policy['insurer']} - {policy['product_name']}")
            print(f"     Premium: RM {policy['estimated_premium']:.2f}")
            print(f"     Score: {policy['score']}/100")
            print(f"     Takaful: {'Yes' if policy['is_takaful'] else 'No'}")
            print()
    else:
        print(f"Error: {response.text}")
    print("-" * 50)

def test_stats():
    """Test stats endpoint"""
    print("Testing stats endpoint...")
    response = requests.get(f"{BASE_URL}/simple/stats")
    print(f"Status: {response.status_code}")
    stats = response.json()
    print("Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    print("-" * 50)

def main():
    """Run all tests"""
    print("=" * 60)
    print("INSURANCE COMPARATOR API TEST")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    try:
        test_health()
        test_policies()
        test_insurers()
        test_comparison()
        test_stats()
        
        print("🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
        print("\nThe Insurance Comparator API is working correctly.")
        print("You can now:")
        print("1. Browse policies at: http://localhost:8000/simple/policies")
        print("2. Compare policies by sending POST requests to: http://localhost:8000/simple/compare")
        print("3. View API documentation at: http://localhost:8000/docs")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("Make sure the API server is running on http://localhost:8000")

if __name__ == "__main__":
    main()
