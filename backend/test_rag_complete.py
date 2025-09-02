#!/usr/bin/env python3
"""
Complete RAG Chain Test Script for InsureWiz with insurewiz768 index
This script tests the entire RAG pipeline from document ingestion to AI response generation
"""

import asyncio
import sys
import os
import time

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.services.ai_service import ai_service
from app.services.vector_store import vector_store_service
from app.services.document_service import document_service
from app.services.project_document_service import project_document_service
from app.services.embedding_service import embedding_service
from app.utils.logger import setup_logger

logger = setup_logger("test_rag_complete")

class RAGCompletenessTester:
    """Comprehensive RAG system tester"""
    
    def __init__(self):
        self.test_results = {}
        self.start_time = time.time()
    
    async def test_index_connection(self):
        """Test connection to the new insurewiz768 index"""
        print("🔗 Testing Pinecone Index Connection...")
        
        try:
            # Test index stats
            stats = vector_store_service.get_index_stats()
            print(f"✅ Successfully connected to index: {stats.get('name', 'insurewiz768')}")
            print(f"   Total vectors: {stats.get('total_vector_count', 0)}")
            print(f"   Dimension: {stats.get('dimension', 0)}")
            print(f"   Metric: {stats.get('metric', 'unknown')}")
            
            # Check namespaces
            namespaces = stats.get('namespaces', {})
            if namespaces:
                print(f"   Available namespaces: {list(namespaces.keys())}")
            else:
                print("   No namespaces found (this is normal for a new index)")
            
            self.test_results['index_connection'] = True
            return True
            
        except Exception as e:
            print(f"❌ Index connection failed: {str(e)}")
            self.test_results['index_connection'] = False
            return False
    
    async def test_embedding_service(self):
        """Test the embedding service functionality"""
        print("\n🧮 Testing Embedding Service...")
        
        try:
            # Test document embeddings
            test_texts = [
                "Malaysian motor insurance provides comprehensive coverage for vehicles",
                "The InsureWiz project uses AI and vector databases for knowledge retrieval",
                "Health insurance covers medical expenses and hospitalization costs"
            ]
            
            embeddings = embedding_service.embed_documents(test_texts)
            if embeddings and len(embeddings) == 3:
                print(f"✅ Document embeddings: {len(embeddings[0])} dimensions")
            else:
                print("❌ Document embeddings failed")
                return False
            
            # Test query embedding
            query_embedding = embedding_service.embed_query("What is motor insurance?")
            if query_embedding and len(query_embedding) > 0:
                print(f"✅ Query embedding: {len(query_embedding)} dimensions")
            else:
                print("❌ Query embedding failed")
                return False
            
            self.test_results['embedding_service'] = True
            return True
            
        except Exception as e:
            print(f"❌ Embedding service test failed: {str(e)}")
            self.test_results['embedding_service'] = False
            return False
    
    async def test_knowledge_base_ingestion(self):
        """Test knowledge base document ingestion"""
        print("\n📚 Testing Knowledge Base Ingestion...")
        
        try:
            # Initialize insurance knowledge base
            print("   Initializing insurance knowledge base...")
            insurance_success = await ai_service.initialize_knowledge_base()
            
            if insurance_success:
                print("✅ Insurance knowledge base initialized")
            else:
                print("⚠️ Insurance knowledge base initialization failed")
            
            # Initialize project knowledge base
            print("   Initializing project knowledge base...")
            project_success = await ai_service.initialize_project_knowledge_base()
            
            if project_success:
                print("✅ Project knowledge base initialized")
            else:
                print("⚠️ Project knowledge base initialization failed")
            
            # Check index stats after ingestion
            stats = vector_store_service.get_index_stats()
            total_vectors = stats.get('total_vector_count', 0)
            print(f"   Total vectors in index: {total_vectors}")
            
            if total_vectors > 0:
                print("✅ Knowledge base ingestion successful")
                self.test_results['knowledge_base_ingestion'] = True
                return True
            else:
                print("❌ No vectors found after ingestion")
                self.test_results['knowledge_base_ingestion'] = False
                return False
                
        except Exception as e:
            print(f"❌ Knowledge base ingestion failed: {str(e)}")
            self.test_results['knowledge_base_ingestion'] = False
            return False
    
    async def test_similarity_search_completeness(self):
        """Test similarity search completeness across different query types"""
        print("\n🔍 Testing Similarity Search Completeness...")
        
        # Test queries for different knowledge domains
        test_queries = [
            # Insurance knowledge queries
            ("What is motor insurance?", "insurance_knowledge", "Should find motor insurance coverage information"),
            ("How do I make a claim?", "insurance_knowledge", "Should find claims process information"),
            ("What is Takaful?", "insurance_knowledge", "Should find Takaful/Islamic insurance information"),
            ("Tell me about health insurance", "insurance_knowledge", "Should find health insurance coverage details"),
            ("What is NCD in insurance?", "insurance_knowledge", "Should find No Claim Discount information"),
            
            # Project knowledge queries
            ("What is InsureWiz?", "project_knowledge", "Should find project overview information"),
            ("How do I run the backend?", "project_knowledge", "Should find setup and running instructions"),
            ("What is the project architecture?", "project_knowledge", "Should find technical architecture details"),
            ("How do I configure the system?", "project_knowledge", "Should find configuration instructions"),
            ("What APIs are available?", "project_knowledge", "Should find API documentation")
        ]
        
        successful_searches = 0
        total_searches = len(test_queries)
        
        for query, expected_namespace, description in test_queries:
            print(f"\n   Query: {query}")
            print(f"   Expected: {description}")
            
            try:
                # Search in specific namespace
                results = vector_store_service.similarity_search(query, namespace=expected_namespace)
                
                if results and len(results) > 0:
                    print(f"   ✅ Found {len(results)} relevant documents")
                    successful_searches += 1
                    
                    # Show first result preview
                    first_result = results[0]
                    print(f"   📄 First result: {first_result.page_content[:100]}...")
                    print(f"   🏷️ Source: {first_result.metadata.get('source', 'Unknown')}")
                else:
                    print(f"   ⚠️ No results found in {expected_namespace}")
                    
            except Exception as e:
                print(f"   ❌ Search failed: {str(e)}")
        
        # Calculate completeness score
        completeness_score = (successful_searches / total_searches) * 100
        print(f"\n   📊 Similarity Search Completeness: {completeness_score:.1f}% ({successful_searches}/{total_searches})")
        
        if completeness_score >= 80:
            print("   🎯 Excellent completeness! RAG system is working well.")
            self.test_results['similarity_search_completeness'] = True
        elif completeness_score >= 60:
            print("   ⚠️ Good completeness, but some areas need improvement.")
            self.test_results['similarity_search_completeness'] = True
        else:
            print("   ❌ Low completeness. RAG system needs attention.")
            self.test_results['similarity_search_completeness'] = False
        
        return completeness_score >= 60
    
    async def test_rag_response_generation(self):
        """Test complete RAG response generation"""
        print("\n🤖 Testing RAG Response Generation...")
        
        test_queries = [
            ("What is comprehensive motor insurance coverage?", "Should generate detailed response about motor insurance"),
            ("How does the InsureWiz project work?", "Should generate response about project architecture"),
            ("What are the different types of health insurance?", "Should generate response about health coverage options"),
            ("How do I set up the development environment?", "Should generate response about project setup")
        ]
        
        successful_rag = 0
        total_queries = len(test_queries)
        
        for query, description in test_queries:
            print(f"\n   Query: {query}")
            print(f"   Expected: {description}")
            
            try:
                # Generate RAG response
                rag_response = await ai_service.generate_rag_response(query)
                
                if rag_response and rag_response.get("rag_used"):
                    print(f"   ✅ RAG response generated successfully")
                    print(f"   📚 Knowledge type: {rag_response.get('knowledge_type')}")
                    print(f"   📄 Context docs: {rag_response.get('context_docs')}")
                    print(f"   💬 Response preview: {rag_response.get('response', '')[:150]}...")
                    successful_rag += 1
                else:
                    print(f"   ⚠️ RAG fell back to basic response")
                    if rag_response:
                        print(f"   💬 Basic response: {rag_response.get('response', '')[:150]}...")
                    
            except Exception as e:
                print(f"   ❌ RAG response generation failed: {str(e)}")
        
        # Calculate RAG effectiveness
        rag_effectiveness = (successful_rag / total_queries) * 100
        print(f"\n   📊 RAG Effectiveness: {rag_effectiveness:.1f}% ({successful_rag}/{total_queries})")
        
        if rag_effectiveness >= 70:
            print("   🎯 Excellent RAG performance!")
            self.test_results['rag_response_generation'] = True
        elif rag_effectiveness >= 50:
            print("   ⚠️ Good RAG performance, but room for improvement.")
            self.test_results['rag_response_generation'] = True
        else:
            print("   ❌ RAG performance needs improvement.")
            self.test_results['rag_response_generation'] = False
        
        return rag_effectiveness >= 50
    
    async def test_cross_namespace_search(self):
        """Test search across different namespaces"""
        print("\n🌐 Testing Cross-Namespace Search...")
        
        try:
            # Test search without specifying namespace (should search across all)
            query = "insurance coverage types"
            results = vector_store_service.similarity_search(query, namespace="")
            
            if results and len(results) > 0:
                print(f"✅ Cross-namespace search successful: found {len(results)} results")
                
                # Check if results come from different namespaces
                sources = set()
                for result in results:
                    source = result.metadata.get('source', 'Unknown')
                    sources.add(source)
                
                print(f"   📚 Sources found: {len(sources)} different sources")
                if len(sources) > 1:
                    print("   🎯 Multiple knowledge sources successfully retrieved")
                else:
                    print("   ⚠️ Only single source found")
                
                self.test_results['cross_namespace_search'] = True
                return True
            else:
                print("❌ Cross-namespace search failed")
                self.test_results['cross_namespace_search'] = False
                return False
                
        except Exception as e:
            print(f"❌ Cross-namespace search test failed: {str(e)}")
            self.test_results['cross_namespace_search'] = False
            return False
    
    async def run_complete_test_suite(self):
        """Run the complete RAG test suite"""
        print("🚀 InsureWiz RAG Completeness Test Suite")
        print("=" * 60)
        print(f"Target Index: insurewiz768")
        print(f"Start Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        tests = [
            ("Index Connection", self.test_index_connection),
            ("Embedding Service", self.test_embedding_service),
            ("Knowledge Base Ingestion", self.test_knowledge_base_ingestion),
            ("Similarity Search Completeness", self.test_similarity_search_completeness),
            ("RAG Response Generation", self.test_rag_response_generation),
            ("Cross-Namespace Search", self.test_cross_namespace_search)
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            print(f"\n{'='*20} {test_name} {'='*20}")
            try:
                if await test_func():
                    passed += 1
                    print(f"✅ {test_name} PASSED")
                else:
                    print(f"❌ {test_name} FAILED")
            except Exception as e:
                print(f"💥 {test_name} CRASHED: {str(e)}")
                self.test_results[test_name.lower().replace(' ', '_')] = False
        
        # Final results
        print("\n" + "=" * 60)
        print("📊 FINAL TEST RESULTS")
        print("=" * 60)
        print(f"Tests Passed: {passed}/{total}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        print(f"Total Time: {time.time() - self.start_time:.2f} seconds")
        
        if passed == total:
            print("\n🎉 ALL TESTS PASSED! RAG system is complete and working correctly.")
        elif passed >= total * 0.8:
            print("\n✅ MOST TESTS PASSED! RAG system is mostly complete with minor issues.")
        else:
            print("\n⚠️ MANY TESTS FAILED! RAG system needs significant attention.")
        
        # Detailed results
        print("\n📋 Detailed Results:")
        for test_name, test_func in tests:
            test_key = test_name.lower().replace(' ', '_')
            status = "✅ PASS" if self.test_results.get(test_key, False) else "❌ FAIL"
            print(f"   {test_name}: {status}")
        
        return passed == total

async def main():
    """Main function to run the complete RAG test suite"""
    tester = RAGCompletenessTester()
    
    try:
        success = await tester.run_complete_test_suite()
        
        if success:
            print("\n🎯 RECOMMENDATION: RAG system is ready for production use!")
        else:
            print("\n🔧 RECOMMENDATION: Review failed tests and fix issues before production use.")
            
    except Exception as e:
        print(f"\n💥 Test suite crashed: {str(e)}")
        print("Check your configuration and ensure all services are running properly.")

if __name__ == "__main__":
    asyncio.run(main())

