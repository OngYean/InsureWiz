#!/usr/bin/env python3
"""
Debug script to test RAG system components individually
"""

import asyncio
import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.services.vector_store import vector_store_service
from app.services.document_service import document_service
from app.services.ai_service import ai_service
from app.utils.logger import setup_logger

logger = setup_logger("rag_debug")

async def test_vector_store():
    """Test vector store functionality"""
    print("=== Testing Vector Store ===")
    try:
        # Test basic functionality
        print("✓ Vector store service imported successfully")
        
        # Test index stats
        stats = vector_store_service.get_index_stats()
        print(f"✓ Index stats retrieved: {stats}")
        
        # Test similarity search
        test_query = "What is InsureWiz?"
        results = vector_store_service.similarity_search(test_query, namespace="project_knowledge")
        print(f"✓ Similarity search successful: Found {len(results)} results")
        
        if results:
            print(f"  First result source: {results[0].metadata.get('source', 'Unknown')}")
            print(f"  First result preview: {results[0].page_content[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"✗ Vector store test failed: {str(e)}")
        return False

async def test_document_service():
    """Test document service functionality"""
    print("\n=== Testing Document Service ===")
    try:
        # Test basic functionality
        print("✓ Document service imported successfully")
        
        # Test knowledge base search
        test_query = "What is InsureWiz?"
        results = document_service.search_knowledge(test_query)
        print(f"✓ Insurance knowledge search successful: Found {len(results)} results")
        
        # Test project knowledge search
        from app.services.project_document_service import project_document_service
        project_results = project_document_service.search_project_knowledge(test_query)
        print(f"✓ Project knowledge search successful: Found {len(results)} results")
        
        return True
        
    except Exception as e:
        print(f"✗ Document service test failed: {str(e)}")
        return False

async def test_ai_service():
    """Test AI service functionality"""
    print("\n=== Testing AI Service ===")
    try:
        # Test basic functionality
        print("✓ AI service imported successfully")
        
        # Test basic response generation
        test_message = "What is insurance?"
        response = await ai_service.generate_response(test_message)
        print(f"✓ Basic AI response generated: {response[:100]}...")
        
        # Test RAG response generation
        rag_response = await ai_service.generate_rag_response(test_message)
        print(f"✓ RAG response generated: {rag_response['response'][:100]}...")
        print(f"  RAG used: {rag_response['rag_used']}")
        print(f"  Context docs: {rag_response['context_docs']}")
        print(f"  Knowledge type: {rag_response['knowledge_type']}")
        
        return True
        
    except Exception as e:
        print(f"✗ AI service test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def test_rag_chain():
    """Test RAG chain specifically"""
    print("\n=== Testing RAG Chain ===")
    try:
        # Check if RAG chain is available
        if ai_service.rag_chain is None:
            print("✗ RAG chain is None - checking why...")
            
            # Try to initialize manually
            print("Attempting to initialize RAG chain manually...")
            ai_service._initialize_rag_chain()
            
            if ai_service.rag_chain is None:
                print("✗ Manual initialization also failed")
                return False
            else:
                print("✓ Manual initialization successful")
        
        print("✓ RAG chain is available")
        return True
        
    except Exception as e:
        print(f"✗ RAG chain test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def test_knowledge_bases():
    """Test knowledge base content"""
    print("\n=== Testing Knowledge Bases ===")
    try:
        # Test insurance knowledge
        print("Testing insurance knowledge...")
        insurance_query = "What is NCD in motor insurance?"
        insurance_results = document_service.search_knowledge(insurance_query)
        print(f"  Insurance results: {len(insurance_results)} documents")
        
        # Test project knowledge
        print("Testing project knowledge...")
        project_query = "What is InsureWiz?"
        from app.services.project_document_service import project_document_service
        project_results = project_document_service.search_project_knowledge(project_query)
        print(f"  Project results: {len(project_results)} documents")
        
        if project_results:
            print(f"  Sample project document source: {project_results[0].metadata.get('source', 'Unknown')}")
            print(f"  Sample project document preview: {project_results[0].page_content[:150]}...")
        
        return True
        
    except Exception as e:
        print(f"✗ Knowledge base test failed: {str(e)}")
        return False

async def main():
    """Run all tests"""
    print("InsureWiz RAG System Debug Test")
    print("=" * 40)
    
    tests = [
        test_vector_store,
        test_document_service,
        test_ai_service,
        test_rag_chain,
        test_knowledge_bases
    ]
    
    results = []
    for test in tests:
        try:
            result = await test()
            results.append(result)
        except Exception as e:
            print(f"✗ Test {test.__name__} failed with exception: {str(e)}")
            results.append(False)
    
    print("\n" + "=" * 40)
    print("Test Results Summary:")
    print(f"Passed: {sum(results)}/{len(results)}")
    print(f"Failed: {len(results) - sum(results)}/{len(results)}")
    
    if all(results):
        print("🎉 All tests passed! RAG system is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")

if __name__ == "__main__":
    asyncio.run(main())
