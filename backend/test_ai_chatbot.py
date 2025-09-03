#!/usr/bin/env python3
"""
Test script for AI Chatbot functionality
Tests different query routing scenarios:
1. InsureWiz project questions -> RAG only
2. Current insurance questions -> RAG + Tavily
3. General questions -> Gemini direct
"""

import asyncio
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

# Add the app directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "app"))

from services.ai_service import ai_service
from utils.logger import default_logger as logger

async def test_ai_chatbot():
    """Test the AI chatbot with different types of questions"""
    
    print("🤖 Testing AI Chatbot Functionality")
    print("=" * 50)
    
    # Test cases for different query types
    test_cases = [
        {
            "category": "InsureWiz Project Questions (RAG only)",
            "questions": [
                "What is InsureWiz?",
                "How do I set up the InsureWiz project?",
                "What are the main features of InsureWiz?",
                "Explain the architecture of InsureWiz"
            ]
        },
        {
            "category": "Current Insurance Questions (RAG + Tavily)",
            "questions": [
                "What are the current car insurance rates in 2024?",
                "What's the latest news about insurance regulations?",
                "What are the current trends in health insurance?",
                "What are today's insurance market conditions?"
            ]
        },
        {
            "category": "General Questions (Gemini direct)",
            "questions": [
                "What is the capital of France?",
                "How does photosynthesis work?",
                "What is the Pythagorean theorem?",
                "Who wrote Romeo and Juliet?"
            ]
        }
    ]
    
    for test_case in test_cases:
        print(f"\n📋 Testing: {test_case['category']}")
        print("-" * 40)
        
        for question in test_case['questions']:
            print(f"\n❓ Question: {question}")
            
            try:
                # Test the intelligent response generation
                response = await ai_service.generate_intelligent_response(question)
                
                print(f"✅ Response generated successfully!")
                print(f"   Strategy: {response.get('strategy', 'Unknown')}")
                print(f"   RAG used: {response.get('rag_used', False)}")
                print(f"   Tavily used: {response.get('tavily_used', False)}")
                print(f"   Knowledge type: {response.get('knowledge_type', 'Unknown')}")
                print(f"   Total sources: {response.get('total_sources', 0)}")
                
                # Show a preview of the response
                response_text = response.get('response', '')
                if response_text:
                    preview = response_text[:200] + "..." if len(response_text) > 200 else response_text
                    print(f"   Response preview: {preview}")
                
            except Exception as e:
                print(f"❌ Error: {str(e)}")
                logger.error(f"Error testing question '{question}': {str(e)}")
        
        print("\n" + "=" * 50)

async def test_query_classification():
    """Test the query intent classification separately"""
    
    print("\n🔍 Testing Query Intent Classification")
    print("=" * 50)
    
    test_questions = [
        "What is InsureWiz?",
        "What are current car insurance rates?",
        "How does photosynthesis work?",
        "What are the project dependencies?",
        "What's the latest insurance news?"
    ]
    
    for question in test_questions:
        try:
            intent = ai_service._classify_query_intent(question)
            print(f"❓ Question: {question}")
            print(f"   Classified as: {intent}")
        except Exception as e:
            print(f"❌ Error classifying '{question}': {str(e)}")
    
    print("\n" + "=" * 50)

async def main():
    """Main test function"""
    try:
        print("🚀 Starting AI Chatbot Tests...")
        
        # Test query classification
        await test_query_classification()
        
        # Test full response generation
        await test_ai_chatbot()
        
        print("\n✅ All tests completed!")
        
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        logger.error(f"Test failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    # Run the tests
    asyncio.run(main())
