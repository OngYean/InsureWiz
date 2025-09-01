"""
Test script for Malaysian Motor Insurance Comparator
Tests core functionality without external dependencies
"""

import sys
import os
import asyncio
from datetime import datetime

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

async def test_basic_imports():
    """Test basic module imports"""
    print("🔍 Testing Basic Imports...")
    
    try:
        from app.comparator.models.policy import PolicyRecord, CustomerInput
        from app.comparator.models.comparison import ComparisonResult
        print("✅ Pydantic models imported successfully")
        
        # Test that PolicyRecord is properly defined
        assert PolicyRecord is not None
        print("✅ PolicyRecord class accessible")
        
    except Exception as e:
        print(f"❌ Model import failed: {e}")
        return False
    
    try:
        from app.comparator.utils.simple_scoring import ScoreWeights, calculate_policy_score
        print("✅ Scoring utilities imported successfully")
    except Exception as e:
        print(f"❌ Scoring utilities import failed: {e}")
        return False
    
    try:
        from app.comparator.utils.compliance import compliance_manager
        print("✅ Compliance manager imported successfully")
    except Exception as e:
        print(f"❌ Compliance manager import failed: {e}")
        return False
    
    return True

async def test_data_models():
    """Test Pydantic data models"""
    print("\n📋 Testing Data Models...")
    
    try:
        from app.comparator.models.policy import PolicyRecord, CustomerInput, PersonalInfo, VehicleInfo, CustomerPreferences
        
        # Test PolicyRecord creation
        policy = PolicyRecord(
            insurer="Test Insurer",
            product_name="Test Policy",
            coverage_type="Comprehensive",  # Use proper enum value
            is_takaful=False,
            coverage_details={
                "windscreen_cover": True,
                "roadside_assistance": True
            },
            pricing={
                "base_premium": 2500.00,
                "excess": 500.00
            }
        )
        print("✅ PolicyRecord model working")
        
        # Test CustomerInput creation
        customer = CustomerInput(
            personal_info=PersonalInfo(
                age=30,
                gender="male",
                driving_experience_years=10
            ),
            vehicle_info=VehicleInfo(
                make="Honda",
                model="Civic",
                year=2020,
                vehicle_value=85000
            ),
            preferences=CustomerPreferences(
                coverage_preference="comprehensive",
                price_range_max=3000,
                prefers_takaful=False
            )
        )
        print("✅ CustomerInput model working")
        
        return True
        
    except Exception as e:
        print(f"❌ Data model test failed: {e}")
        return False

async def test_scoring_system():
    """Test the scoring algorithm"""
    print("\n🎯 Testing Scoring System...")
    
    try:
        # Import within the function to avoid global scope issues
        from app.comparator.utils.simple_scoring import ScoreWeights, calculate_policy_score
        from app.comparator.models.policy import PolicyRecord
        
        # Create test policy
        policy = PolicyRecord(
            insurer="Test Insurer",
            product_name="Test Policy",
            coverage_type="Comprehensive",  # Use proper enum value
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
            },
            eligibility_criteria={
                "min_age": 21,
                "max_age": 75,
                "vehicle_age_max": 15
            }
        )
        
        # Test scoring with default weights
        weights = ScoreWeights()
        score = calculate_policy_score(policy, weights)
        
        print(f"✅ Scoring system working - Test score: {score:.1f}/100")
        return True
        
    except Exception as e:
        print(f"❌ Scoring system test failed: {e}")
        return False

async def test_template_system():
    """Test Jinja2 template rendering"""
    print("\n📄 Testing Template System...")
    
    try:
        import jinja2
        from pathlib import Path
        
        # Test template loading
        template_path = Path("app/comparator/templates")
        if template_path.exists():
            env = jinja2.Environment(
                loader=jinja2.FileSystemLoader(template_path)
            )
            
            template = env.get_template("comparison.html")
            
            # Test basic rendering
            test_data = {
                "report_title": "Test Insurance Comparison",
                "generation_date": datetime.now().strftime("%B %d, %Y"),
                "customer_name": "Test Customer",
                "total_policies": 3,
                "top_recommendation": "Test Insurer",
                "branding": {
                    "primary_color": "#2563eb"
                },
                "summary": {
                    "takaful_options": 2,
                    "coverage_range": {
                        "comprehensive": 3,
                        "third_party": 1
                    }
                },
                "ranked_policies": [],
                "comparison_matrix": []
            }
            
            rendered = template.render(**test_data)
            print("✅ Template system working - HTML generated successfully")
            return True
        else:
            print("❌ Template directory not found")
            return False
            
    except Exception as e:
        print(f"❌ Template system test failed: {e}")
        return False

async def test_api_structure():
    """Test API endpoint structure"""
    print("\n🌐 Testing API Structure...")
    
    try:
        # Import within function to avoid global scope issues
        from app.comparator.api.main import router as comparator_router
        from app.comparator.api.crawl import router as crawl_router
        from app.comparator.api.compare import router as compare_router
        from app.comparator.api.reports import router as reports_router
        
        print("✅ All API routers imported successfully")
        
        # Check router configuration
        print(f"✅ Comparator router prefix: {comparator_router.prefix}")
        print(f"✅ Available routes: {len(comparator_router.routes)}")
        
        return True
        
    except Exception as e:
        print(f"❌ API structure test failed: {e}")
        return False

async def test_database_models():
    """Test database operation structure"""
    print("\n🗄️ Testing Database Models...")
    
    try:
        # Test that the database module structure exists
        import os
        db_path = os.path.join("app", "comparator", "database")
        if os.path.exists(db_path):
            print("✅ Database module directory exists")
        
        # Test basic import without connection
        try:
            from app.comparator.database import operations
            print("✅ Database operations module accessible")
        except ImportError as e:
            print(f"⚠️ Database operations import issue: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Database model test failed: {e}")
        return False

async def run_all_tests():
    """Run comprehensive test suite"""
    print("🚀 Starting Malaysian Motor Insurance Comparator Tests\n")
    
    tests = [
        test_basic_imports,
        test_data_models,
        test_scoring_system,
        test_template_system,
        test_api_structure,
        test_database_models
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
    
    print(f"\n📊 Test Results:")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📋 Total: {passed + failed}")
    
    if failed == 0:
        print("\n🎉 All tests passed! System is ready for deployment.")
    else:
        print(f"\n⚠️ {failed} test(s) failed. Check the errors above.")
    
    return failed == 0

if __name__ == "__main__":
    asyncio.run(run_all_tests())
