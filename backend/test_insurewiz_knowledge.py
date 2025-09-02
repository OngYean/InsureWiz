#!/usr/bin/env python3
"""
Test script to verify InsureWiz knowledge retrieval
"""

import asyncio
import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.services.ai_service import ai_service
from app.services.vector_store import vector_store_service
from app.utils.logger import setup_logger

logger = setup_logger("test_insurewiz_knowledge")

async def test_insurewiz_knowledge_retrieval():
    """Test that queries about InsureWiz return relevant information"""
    print("🔍 Testing InsureWiz Knowledge Retrieval...\n")
    
    # Test queries about InsureWiz
    test_queries = [
        "What is InsureWiz?",
        "How does InsureWiz work?",
        "What is the architecture of InsureWiz?",
        "How do I set up InsureWiz?",
        "What technologies does InsureWiz use?",
        "How do I run InsureWiz?",
        "What are the main features of InsureWiz?",
        "How do I deploy InsureWiz?",
        "What is the project structure of InsureWiz?",
        "How do I configure InsureWiz?"
    ]
    
    successful_queries = 0
    total_queries = len(test_queries)
    
    for i, query in enumerate(test_queries, 1):
        print(f"Query {i}/{total_queries}: {query}")
        
        try:
            # Generate RAG response
            response = await ai_service.generate_rag_response(query)
            
            if response and response.get("rag_used"):
                print(f"✅ RAG Response (Knowledge Type: {response.get('knowledge_type')})")
                print(f"   Context Docs: {response.get('context_docs')}")
                print(f"   Response: {response.get('response', '')[:200]}...")
                successful_queries += 1
            else:
                print(f"⚠️ Basic Response (No RAG)")
                print(f"   Response: {response.get('response', '')[:200]}...")
            
            print("-" * 80)
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            print("-" * 80)
    
    print(f"\n📊 Knowledge Retrieval Results: {successful_queries}/{total_queries} queries used RAG")
    
    if successful_queries > 0:
        print("🎉 InsureWiz knowledge retrieval is working!")
    else:
        print("⚠️ No queries used RAG. This may indicate the knowledge base needs to be populated.")

async def test_specific_insurewiz_features():
    """Test specific InsureWiz features and capabilities"""
    print("\n🚀 Testing Specific InsureWiz Features...\n")
    
    feature_tests = [
        {
            "query": "What is the main purpose of InsureWiz?",
            "expected_keywords": ["insurance", "advisor", "chatbot", "malaysian", "takaful"]
        },
        {
            "query": "What AI model does InsureWiz use?",
            "expected_keywords": ["gemini", "google", "ai", "model"]
        },
        {
            "query": "What database does InsureWiz use for vector storage?",
            "expected_keywords": ["pinecone", "vector", "database", "storage"]
        },
        {
            "query": "How does InsureWiz handle insurance knowledge?",
            "expected_keywords": ["knowledge", "base", "retrieval", "rag", "vector"]
        }
    ]
    
    for test in feature_tests:
        print(f"Testing: {test['query']}")
        
        try:
            response = await ai_service.generate_rag_response(test['query'])
            response_text = response.get('response', '').lower()
            
            # Check if expected keywords are present
            found_keywords = [keyword for keyword in test['expected_keywords'] if keyword in response_text]
            
            if found_keywords:
                print(f"✅ Found relevant keywords: {found_keywords}")
            else:
                print(f"⚠️ Missing expected keywords. Found: {response_text[:100]}...")
            
            print("-" * 60)
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            print("-" * 60)

async def main():
    """Main test function"""
    print("🧪 InsureWiz Knowledge Retrieval Test Suite\n")
    
    # Test 1: General knowledge retrieval
    await test_insurewiz_knowledge_retrieval()
    
    # Test 2: Specific feature testing
    await test_specific_insurewiz_features()
    
    print("\n🎯 Test Suite Complete!")
    print("If you see RAG responses with relevant InsureWiz information, the system is working correctly.")

if __name__ == "__main__":
    asyncio.run(main())
