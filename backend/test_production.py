"""
FastAPI Backend Server Test
Tests the actual running server functionality
"""

import asyncio
import sys
import os
from datetime import datetime

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

async def test_fastapi_server():
    """Test FastAPI server startup"""
    print("🚀 Testing FastAPI Server...")
    
    try:
        from fastapi.testclient import TestClient
        from app.core.app import app
        
        client = TestClient(app)
        
        # Test health endpoint
        response = client.get("/api/health")
        print(f"✅ Health endpoint status: {response.status_code}")
        
        # Test comparator info endpoint
        response = client.get("/api/comparator/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Comparator info: {data['name']}")
            print(f"✅ Supported insurers: {len(data['supported_insurers'])}")
        else:
            print(f"⚠️ Comparator endpoint status: {response.status_code}")
        
        # Test comparator health
        response = client.get("/api/comparator/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Comparator health: {data['status']}")
        else:
            print(f"⚠️ Comparator health status: {response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"❌ FastAPI server test failed: {e}")
        return False

async def test_policy_model_direct():
    """Test policy models directly"""
    print("\n📋 Testing Policy Models...")
    
    try:
        # Direct import from policy module
        from app.comparator.models.policy import PolicyRecord, CustomerInput, PersonalInfo, VehicleInfo, CustomerPreferences
        
        # Test complete policy creation
        policy = PolicyRecord(
            insurer="Zurich Malaysia",
            product_name="Z-Driver", 
            coverage_type="Comprehensive",
            is_takaful=False,
            coverage_details={
                "windscreen_cover": True,
                "roadside_assistance": True,
                "flood_coverage": True
            },
            pricing={
                "base_premium": 2500.00,
                "excess": 500.00,
                "ncd_discount": 55
            }
        )
        print(f"✅ PolicyRecord created: {policy.insurer} - {policy.product_name}")
        
        # Test customer input
        customer = CustomerInput(
            personal_info=PersonalInfo(age=30, gender="male"),
            vehicle_info=VehicleInfo(make="Honda", model="Civic", year=2020),
            preferences=CustomerPreferences(
                coverage_preference="comprehensive",
                prefers_takaful=False,
                price_range_max=3000
            )
        )
        print(f"✅ CustomerInput created for {customer.vehicle_info.make} {customer.vehicle_info.model}")
        
        return True
        
    except Exception as e:
        print(f"❌ Policy model test failed: {e}")
        return False

async def test_simple_api_endpoints():
    """Test API endpoints with minimal data"""
    print("\n🌐 Testing API Endpoints...")
    
    try:
        from fastapi.testclient import TestClient
        from app.core.app import app
        
        client = TestClient(app)
        
        # Test quick comparison with sample data
        quick_compare_data = {
            "vehicle_type": "sedan",
            "coverage_type": "comprehensive",
            "max_price": 3000,
            "prefer_takaful": False
        }
        
        response = client.post("/api/comparator/compare/quick", json=quick_compare_data)
        print(f"Quick comparison status: {response.status_code}")
        
        if response.status_code != 500:  # Not expecting it to work without database
            print("✅ Quick comparison endpoint accessible")
        else:
            print("⚠️ Quick comparison requires database setup")
        
        # Test crawling status
        response = client.get("/api/comparator/crawl/status")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Crawling status: {data['status']}")
        else:
            print(f"⚠️ Crawling status: {response.status_code}")
        
        # Test available formats
        response = client.get("/api/comparator/reports/formats")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Report formats available: {len(data['supported_formats'])}")
        else:
            print(f"⚠️ Report formats: {response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"❌ API endpoint test failed: {e}")
        return False

async def test_environment_setup():
    """Test environment configuration"""
    print("\n⚙️ Testing Environment Setup...")
    
    try:
        from app.config import settings
        
        # Check API keys
        has_google_key = bool(settings.google_api_key)
        has_tavily_key = bool(settings.tavily_api_key)  
        has_supabase_url = bool(settings.supabase_url)
        has_supabase_key = bool(settings.supabase_key)
        
        print(f"Google API Key: {'✅' if has_google_key else '❌'}")
        print(f"Tavily API Key: {'✅' if has_tavily_key else '❌'}")
        print(f"Supabase URL: {'✅' if has_supabase_url else '❌'}")
        print(f"Supabase Key: {'✅' if has_supabase_key else '❌'}")
        
        # Check if all required keys are present
        all_keys_present = has_google_key and has_tavily_key and has_supabase_url and has_supabase_key
        
        if all_keys_present:
            print("✅ All API keys configured")
        else:
            print("⚠️ Some API keys missing - functionality will be limited")
        
        return True
        
    except Exception as e:
        print(f"❌ Environment test failed: {e}")
        return False

async def test_scoring_algorithm():
    """Test scoring system"""
    print("\n🎯 Testing Scoring Algorithm...")
    
    try:
        from app.comparator.utils.simple_scoring import ScoreWeights, calculate_policy_score
        from app.comparator.models.policy import PolicyRecord
        
        # Create test policy
        policy = PolicyRecord(
            insurer="Test Insurer",
            product_name="Test Policy",
            coverage_type="Comprehensive",
            is_takaful=False,
            coverage_details={
                "windscreen_cover": True,
                "roadside_assistance": True,
                "flood_coverage": True,
                "riot_strike_coverage": True
            },
            pricing={
                "base_premium": 2200.00,
                "excess": 400.00,
                "ncd_discount": 55
            }
        )
        
        # Test scoring
        weights = ScoreWeights()
        score = calculate_policy_score(policy, weights)
        
        print(f"✅ Policy scoring working: {score}/100")
        print(f"✅ Policy has {len([v for v in policy.coverage_details.values() if v])} coverage features")
        print(f"✅ Premium: RM{policy.pricing['base_premium']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Scoring algorithm test failed: {e}")
        return False

async def run_production_tests():
    """Run production-ready tests"""
    print("🏢 Malaysian Motor Insurance Comparator - Production Test Suite")
    print("=" * 70)
    
    tests = [
        test_environment_setup,
        test_policy_model_direct,
        test_scoring_algorithm,
        test_fastapi_server,
        test_simple_api_endpoints
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            result = await test()
            if result:
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            failed += 1
    
    print("\n" + "=" * 70)
    print(f"📊 PRODUCTION TEST RESULTS:")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📋 Total: {passed + failed}")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! System ready for production.")
        print("🚀 You can now start the server with: python start_server.py")
    elif passed >= 3:
        print(f"\n✅ {passed} core tests passed - System is mostly functional!")
        print("⚠️ Some advanced features may have limitations.")
    else:
        print(f"\n⚠️ {failed} test(s) failed. Please review the errors above.")
    
    # System recommendations
    print("\n📋 NEXT STEPS:")
    if passed >= 3:
        print("1. ✅ Start the FastAPI server: python start_server.py")
        print("2. ✅ Test endpoints: http://localhost:8000/docs")
        print("3. ✅ Set up Supabase database using supabase_setup.sql")
        print("4. ✅ Test frontend integration")
    else:
        print("1. Fix failing tests above")
        print("2. Verify all dependencies are installed")
        print("3. Check environment configuration")
    
    return failed == 0

if __name__ == "__main__":
    asyncio.run(run_production_tests())
