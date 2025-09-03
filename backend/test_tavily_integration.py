#!/usr/bin/env python3
"""
Test script for Tavily integration in InsureWiz chatbot
"""

import asyncio
import os
import sys
from dotenv import load_dotenv

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

# Load environment variables
load_dotenv()

async def test_tavily_service():
    """Test the Tavily service functionality"""
    print("🧪 Testing Tavily Service Integration...")
    print("=" * 50)
    
    try:
        from app.services.tavily_service import tavily_service
        
        # Test 1: Check if service is enabled
        print("\n1. Testing service availability...")
        is_enabled = tavily_service.is_enabled()
        print(f"   Tavily service enabled: {is_enabled}")
        
        if not is_enabled:
            print("   ⚠️  Tavily service not enabled. Check your TAVILY_API_KEY in .env file")
            return False
        
        # Test 2: Health check
        print("\n2. Testing service health...")
        health_status = await tavily_service.health_check()
        print(f"   Status: {health_status.get('status', 'unknown')}")
        print(f"   Message: {health_status.get('message', 'No message')}")
        
        # Test 3: Basic search
        print("\n3. Testing basic search...")
        search_results = await tavily_service.search("Malaysia insurance market trends 2024", max_results=3)
        print(f"   Found {len(search_results)} results")
        
        if search_results:
            print("   Sample result:")
            first_result = search_results[0]
            print(f"   - Title: {first_result.get('title', 'No title')}")
            print(f"   - Source: {first_result.get('source', 'Unknown')}")
            print(f"   - Content preview: {first_result.get('content', '')[:100]}...")
        
        # Test 4: Insurance-specific search
        print("\n4. Testing insurance-specific search...")
        insurance_results = await tavily_service.search_insurance_related("motor insurance NCD")
        print(f"   Found {len(insurance_results)} insurance-related results")
        
        # Test 5: Market trends search
        print("\n5. Testing market trends search...")
        trend_results = await tavily_service.search_market_trends("motor")
        print(f"   Found {len(trend_results)} market trend results")
        
        print("\n✅ All Tavily service tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error testing Tavily service: {str(e)}")
        return False

async def test_enhanced_ai_service():
    """Test the enhanced AI service with Tavily integration"""
    print("\n🧪 Testing Enhanced AI Service...")
    print("=" * 50)
    
    try:
        from app.services.ai_service import ai_service
        
        # Test enhanced response generation
        test_query = "What are the current motor insurance rates in Malaysia for 2024?"
        print(f"\nTesting enhanced response for: '{test_query}'")
        
        enhanced_response = await ai_service.generate_enhanced_response(test_query, use_tavily=True)
        
        print(f"   Response generated: {'Yes' if enhanced_response.get('response') else 'No'}")
        print(f"   RAG used: {enhanced_response.get('rag_used', False)}")
        print(f"   Tavily used: {enhanced_response.get('tavily_used', False)}")
        print(f"   Total sources: {enhanced_response.get('total_sources', 0)}")
        print(f"   Web sources: {len(enhanced_response.get('web_sources', []))}")
        
        if enhanced_response.get('web_sources'):
            print("   Web sources found:")
            for i, source in enumerate(enhanced_response['web_sources'][:2], 1):
                print(f"     {i}. {source.get('title', 'No title')} - {source.get('source', 'Unknown')}")
        
        print("\n✅ Enhanced AI service test completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error testing enhanced AI service: {str(e)}")
        return False

async def main():
    """Main test function"""
    print("🚀 InsureWiz Tavily Integration Test")
    print("=" * 50)
    
    # Check environment variables
    print("\n📋 Environment Check:")
    tavily_key = os.getenv("TAVILY_API_KEY")
    if tavily_key:
        print("   ✅ TAVILY_API_KEY found")
    else:
        print("   ❌ TAVILY_API_KEY not found in environment")
        print("   Please add TAVILY_API_KEY=your_key_here to your .env file")
        return
    
    # Run tests
    tavily_success = await test_tavily_service()
    ai_success = await test_enhanced_ai_service()
    
    # Summary
    print("\n📊 Test Summary:")
    print("=" * 50)
    print(f"   Tavily Service: {'✅ PASS' if tavily_success else '❌ FAIL'}")
    print(f"   Enhanced AI Service: {'✅ PASS' if ai_success else '❌ FAIL'}")
    
    if tavily_success and ai_success:
        print("\n🎉 All tests passed! Tavily integration is working correctly.")
        print("\nYou can now use the enhanced endpoints:")
        print("   - POST /api/chat/enhanced - For enhanced RAG + Tavily responses")
        print("   - GET /api/chat/tavily-health - To check service health")
    else:
        print("\n⚠️  Some tests failed. Please check the error messages above.")
        print("Make sure your Tavily API key is valid and the service is accessible.")

if __name__ == "__main__":
    asyncio.run(main())

