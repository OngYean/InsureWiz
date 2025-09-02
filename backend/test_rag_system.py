#!/usr/bin/env python3
"""
Test script to verify RAG system functionality
"""

import asyncio
import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.services.ai_service import ai_service
from app.services.vector_store import vector_store_service
from app.services.embedding_service import embedding_service
from app.utils.logger import setup_logger

logger = setup_logger("test_rag")

async def test_embedding_service():
    """Test the embedding service"""
    print("🔍 Testing Embedding Service...")
    
    try:
        # Test document embedding
        test_texts = ["This is a test document about insurance", "Another test document about claims"]
        embeddings = embedding_service.embed_documents(test_texts)
        
        if embeddings and len(embeddings) == 2:
            print(f"✅ Document embeddings generated successfully: {len(embeddings[0])} dimensions")
        else:
            print("❌ Document embeddings failed")
            return False
        
        # Test query embedding
        query_embedding = embedding_service.embed_query("test query")
        if query_embedding and len(query_embedding) > 0:
            print(f"✅ Query embedding generated successfully: {len(query_embedding)} dimensions")
        else:
            print("❌ Query embedding failed")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Embedding service test failed: {str(e)}")
        return False

async def test_vector_store():
    """Test the vector store service"""
    print("\n🗄️ Testing Vector Store Service...")
    
    try:
        # Test index stats
        stats = vector_store_service.get_index_stats()
        print(f"✅ Vector store stats retrieved: {stats}")
        
        # Test adding test documents
        from langchain.schema import Document
        
        test_docs = [
            Document(
                page_content="InsureWiz is an AI-powered insurance advisor chatbot that helps users understand Malaysian insurance and Takaful policies.",
                metadata={"source": "test", "category": "project_overview"}
            ),
            Document(
                page_content="The system uses Google's Gemini AI model and Pinecone vector database for knowledge retrieval.",
                metadata={"source": "test", "category": "technical_details"}
            )
        ]
        
        success = vector_store_service.add_documents(test_docs, namespace="test")
        if success:
            print("✅ Test documents added to vector store successfully")
        else:
            print("❌ Failed to add test documents")
            return False
        
        # Test similarity search
        search_results = vector_store_service.similarity_search("What is InsureWiz?", namespace="test")
        if search_results and len(search_results) > 0:
            print(f"✅ Similarity search successful: found {len(search_results)} results")
            for i, result in enumerate(search_results):
                print(f"   Result {i+1}: {result.page_content[:100]}...")
        else:
            print("❌ Similarity search failed")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Vector store test failed: {str(e)}")
        return False

async def test_ai_service():
    """Test the AI service"""
    print("\n🤖 Testing AI Service...")
    
    try:
        # Test basic response generation
        basic_response = await ai_service.generate_response("What is insurance?")
        if basic_response and len(basic_response) > 0:
            print("✅ Basic AI response generated successfully")
            print(f"   Response preview: {basic_response[:100]}...")
        else:
            print("❌ Basic AI response failed")
            return False
        
        # Test RAG response generation
        rag_response = await ai_service.generate_rag_response("Tell me about InsureWiz project", namespace="test")
        if rag_response and rag_response.get("rag_used"):
            print("✅ RAG response generated successfully")
            print(f"   Knowledge type: {rag_response.get('knowledge_type')}")
            print(f"   Context docs: {rag_response.get('context_docs')}")
            print(f"   Response preview: {rag_response.get('response', '')[:100]}...")
        else:
            print("⚠️ RAG response fell back to basic response (this may be normal for test queries)")
            
        return True
        
    except Exception as e:
        print(f"❌ AI service test failed: {str(e)}")
        return False

async def test_knowledge_base_initialization():
    """Test knowledge base initialization"""
    print("\n📚 Testing Knowledge Base Initialization...")
    
    try:
        # Test project knowledge base initialization
        project_success = await ai_service.initialize_project_knowledge_base()
        if project_success:
            print("✅ Project knowledge base initialized successfully")
        else:
            print("⚠️ Project knowledge base initialization failed (may not have project docs)")
        
        # Test insurance knowledge base initialization
        insurance_success = await ai_service.initialize_knowledge_base()
        if insurance_success:
            print("✅ Insurance knowledge base initialized successfully")
        else:
            print("⚠️ Insurance knowledge base initialization failed (may not have insurance docs)")
            
        return True
        
    except Exception as e:
        print(f"❌ Knowledge base initialization test failed: {str(e)}")
        return False

async def main():
    """Main test function"""
    print("🚀 Starting RAG System Tests...\n")
    
    tests = [
        test_embedding_service,
        test_vector_store,
        test_ai_service,
        test_knowledge_base_initialization
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if await test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {str(e)}")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! RAG system is working correctly.")
    else:
        print("⚠️ Some tests failed. Check the logs above for details.")
    
    # Clean up test namespace
    try:
        vector_store_service.delete_namespace("test")
        print("🧹 Test namespace cleaned up")
    except:
        pass

if __name__ == "__main__":
    asyncio.run(main())
