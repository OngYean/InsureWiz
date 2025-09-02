#!/usr/bin/env python3
"""
Test script to verify similarity search with improved embeddings
"""

import asyncio
import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.services.vector_store import vector_store_service
from app.services.embedding_service import embedding_service
from app.utils.logger import setup_logger

logger = setup_logger("test_similarity")

async def test_similarity_search():
    """Test similarity search with different types of queries"""
    print("🔍 Testing Similarity Search with Improved Embeddings...\n")
    
    # Test queries that should find relevant documents
    test_queries = [
        ("What is insurance?", "insurance_knowledge"),
        ("How do I make a claim?", "insurance_knowledge"),
        ("What is motor insurance?", "insurance_knowledge"),
        ("Tell me about the project structure", "project_knowledge"),
        ("How do I run the backend?", "project_knowledge"),
        ("What is the API setup?", "project_knowledge"),
        ("What is Takaful?", "insurance_knowledge"),
        ("How do I configure the system?", "project_knowledge")
    ]
    
    for query, expected_namespace in test_queries:
        print(f"Query: {query}")
        print(f"Expected namespace: {expected_namespace}")
        
        try:
            # Test search in specific namespace
            results = vector_store_service.similarity_search(query, namespace=expected_namespace)
            
            if results and len(results) > 0:
                print(f"✅ Found {len(results)} relevant documents in {expected_namespace}")
                for i, result in enumerate(results[:2]):  # Show first 2 results
                    print(f"   Result {i+1}: {result.page_content[:100]}...")
                    print(f"   Source: {result.metadata.get('source', 'Unknown')}")
            else:
                print(f"⚠️ No results found in {expected_namespace}")
            
            # Test search across all namespaces
            all_results = vector_store_service.similarity_search(query, namespace="")
            
            if all_results and len(all_results) > 0:
                print(f"✅ Found {len(all_results)} relevant documents across all namespaces")
                for i, result in enumerate(all_results[:2]):  # Show first 2 results
                    print(f"   Result {i+1}: {result.page_content[:100]}...")
                    print(f"   Source: {result.metadata.get('source', 'Unknown')}")
            else:
                print(f"⚠️ No results found across all namespaces")
            
        except Exception as e:
            print(f"❌ Error searching for '{query}': {str(e)}")
        
        print("-" * 80)
    
    # Test embedding similarity between related concepts
    print("\n🧮 Testing Embedding Similarity...")
    
    related_pairs = [
        ("insurance", "policy"),
        ("motor", "car"),
        ("health", "medical"),
        ("project", "code"),
        ("api", "backend"),
        ("database", "storage")
    ]
    
    for word1, word2 in related_pairs:
        try:
            emb1 = embedding_service.embed_query(word1)
            emb2 = embedding_service.embed_query(word2)
            
            # Calculate cosine similarity
            dot_product = sum(a * b for a, b in zip(emb1, emb2))
            magnitude1 = sum(a * a for a in emb1) ** 0.5
            magnitude2 = sum(b * b for b in emb2) ** 0.5
            
            if magnitude1 > 0 and magnitude2 > 0:
                similarity = dot_product / (magnitude1 * magnitude2)
                print(f"Similarity between '{word1}' and '{word2}': {similarity:.4f}")
            else:
                print(f"Similarity between '{word1}' and '{word2}': Cannot calculate")
                
        except Exception as e:
            print(f"❌ Error calculating similarity for '{word1}' and '{word2}': {str(e)}")

async def main():
    """Main test function"""
    print("🧪 Similarity Search Test Suite\n")
    
    await test_similarity_search()
    
    print("\n🎯 Test Suite Complete!")
    print("If you see relevant search results, the improved embeddings are working correctly.")

if __name__ == "__main__":
    asyncio.run(main())
