"""
Test the complete dynamic pipeline: scraping -> transformation -> database storage
"""

import asyncio
import requests
import json
from datetime import datetime


async def test_dynamic_pipeline():
    """Test the complete dynamic pipeline"""
    
    print("🚀 TESTING COMPLETE DYNAMIC PIPELINE")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    
    try:
        # Test the dynamic scraping endpoint
        print("1. Testing dynamic scraping endpoint...")
        response = requests.post(f"{base_url}/dynamic/scrape/all")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Scraping successful!")
            print(f"   📦 Scraped policies: {data.get('scraped_policies', 0)}")
            print(f"   💾 Stored in database: {data.get('stored_in_database', 0)}")
            print(f"   🏢 Insurers processed: {data.get('insurers_processed', 0)}")
            print(f"   🕒 Timestamp: {data.get('timestamp', 'N/A')}")
            
            # Show sample policies
            policies = data.get('policies', [])
            if policies:
                print(f"\n   📋 Sample policies:")
                for i, policy in enumerate(policies[:3]):
                    print(f"      {i+1}. {policy.get('insurer')} - {policy.get('product_name')}")
                    print(f"         Coverage: {policy.get('coverage_type')}")
                    print(f"         Takaful: {'Yes' if policy.get('is_takaful') else 'No'}")
        else:
            print(f"   ❌ Scraping failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return
        
        # Test the live policies endpoint
        print("\n2. Testing live policies endpoint...")
        response = requests.get(f"{base_url}/dynamic/policies/live")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Live policies retrieved!")
            print(f"   📊 Total policies: {data.get('total_policies', 0)}")
            print(f"   🕒 Data freshness: {data.get('data_freshness', 'N/A')}")
            
            policies = data.get('policies', [])
            if policies:
                print(f"\n   📋 Live policies in database:")
                for i, policy in enumerate(policies[:5]):
                    print(f"      {i+1}. {policy.get('insurer')} - {policy.get('product_name')}")
                    print(f"         ID: {policy.get('id', 'N/A')[:8]}...")
                    print(f"         Created: {policy.get('created_at', 'N/A')[:19]}")
        else:
            print(f"   ❌ Live policies failed: {response.status_code}")
            print(f"   Error: {response.text}")
        
        # Test comparison endpoint with live data
        print("\n3. Testing comparison with live data...")
        comparison_data = {
            "customer_input": {
                "vehicle_type": "sedan",
                "coverage_preference": "comprehensive",
                "price_range_max": 3000,
                "prefers_takaful": False
            }
        }
        
        response = requests.post(
            f"{base_url}/dynamic/compare/live",
            json=comparison_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Comparison successful!")
            print(f"   📊 Policies compared: {len(data.get('comparison_results', []))}")
            print(f"   🎯 Recommendation: {data.get('recommendation', {}).get('insurer', 'N/A')}")
            print(f"   🏆 Top score: {data.get('recommendation', {}).get('overall_score', 'N/A')}")
        else:
            print(f"   ❌ Comparison failed: {response.status_code}")
            print(f"   Error: {response.text}")
    
    except Exception as e:
        print(f"❌ Test failed: {e}")


if __name__ == "__main__":
    asyncio.run(test_dynamic_pipeline())
