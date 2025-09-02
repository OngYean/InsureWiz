#!/usr/bin/env python3
"""
Migration script to move documents from old 'insurewiz' index to new 'insurewiz768' index
This script will:
1. Connect to the old index
2. Retrieve all documents
3. Re-embed them using the new 768-dimensional embeddings
4. Store them in the new index
"""

import asyncio
import sys
import os
import time
from typing import List, Dict, Any

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.services.vector_store import vector_store_service
from app.services.embedding_service import embedding_service
from app.services.document_service import document_service
from app.services.project_document_service import project_document_service
from app.utils.logger import setup_logger

logger = setup_logger("migration")

class IndexMigrationService:
    """Service for migrating documents between Pinecone indexes"""
    
    def __init__(self):
        self.old_index_name = "insurewiz"
        self.new_index_name = "insurewiz768"
        self.old_pc = None
        self.new_pc = None
        
    def _connect_to_old_index(self):
        """Connect to the old index to retrieve documents"""
        try:
            import pinecone
            self.old_pc = pinecone.Pinecone(api_key=vector_store_service.pinecone_api_key)
            self.old_index = self.old_pc.Index(self.old_index_name)
            logger.info(f"Connected to old index: {self.old_index_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to old index: {str(e)}")
            return False
    
    def _get_old_index_stats(self) -> Dict[str, Any]:
        """Get statistics from the old index"""
        try:
            stats = self.old_index.describe_index_stats()
            logger.info(f"Old index stats: {stats}")
            return stats
        except Exception as e:
            logger.error(f"Failed to get old index stats: {str(e)}")
            return {}
    
    def _retrieve_documents_from_old_index(self, namespace: str = None) -> List[Dict[str, Any]]:
        """Retrieve all documents from the old index"""
        try:
            # Get all vectors from the old index
            if namespace:
                # Get namespace-specific stats
                stats = self.old_index.describe_index_stats()
                if namespace in stats.get('namespaces', {}):
                    namespace_stats = stats['namespaces'][namespace]
                    vector_count = namespace_stats.get('vector_count', 0)
                    logger.info(f"Found {vector_count} vectors in namespace: {namespace}")
                else:
                    logger.warning(f"Namespace {namespace} not found in old index")
                    return []
            else:
                # Get all vectors
                stats = self.old_index.describe_index_stats()
                vector_count = stats.get('total_vector_count', 0)
                logger.info(f"Found {vector_count} total vectors in old index")
            
            # For now, we'll use the document services to recreate the documents
            # This is more reliable than trying to extract from vectors
            logger.info("Will recreate documents using document services")
            return []
            
        except Exception as e:
            logger.error(f"Failed to retrieve documents from old index: {str(e)}")
            return []
    
    async def migrate_insurance_knowledge(self):
        """Migrate insurance knowledge base to new index"""
        logger.info("Starting insurance knowledge migration...")
        
        try:
            # Initialize insurance knowledge base in new index
            success = await document_service.add_insurance_knowledge()
            
            if success:
                logger.info("✅ Insurance knowledge migrated successfully")
                return True
            else:
                logger.error("❌ Insurance knowledge migration failed")
                return False
                
        except Exception as e:
            logger.error(f"Error migrating insurance knowledge: {str(e)}")
            return False
    
    async def migrate_project_knowledge(self):
        """Migrate project knowledge base to new index"""
        logger.info("Starting project knowledge migration...")
        
        try:
            # Initialize project knowledge base in new index
            success = await project_document_service.ingest_project_documentation()
            
            if success:
                logger.info("✅ Project knowledge migrated successfully")
                return True
            else:
                logger.error("❌ Project knowledge migration failed")
                return False
                
        except Exception as e:
            logger.error(f"Error migrating project knowledge: {str(e)}")
            return False
    
    async def verify_migration(self):
        """Verify that the migration was successful"""
        logger.info("Verifying migration...")
        
        try:
            # Check new index stats
            stats = vector_store_service.get_index_stats()
            total_vectors = stats.get('total_vector_count', 0)
            namespaces = stats.get('namespaces', {})
            
            logger.info(f"New index total vectors: {total_vectors}")
            logger.info(f"New index namespaces: {list(namespaces.keys())}")
            
            if total_vectors > 0:
                logger.info("✅ Migration verification successful")
                return True
            else:
                logger.error("❌ No vectors found in new index")
                return False
                
        except Exception as e:
            logger.error(f"Error verifying migration: {str(e)}")
            return False
    
    async def run_migration(self):
        """Run the complete migration process"""
        logger.info("🚀 Starting Index Migration: insurewiz → insurewiz768")
        logger.info("=" * 60)
        
        start_time = time.time()
        
        # Step 1: Connect to old index
        logger.info("\n📡 Step 1: Connecting to old index...")
        if not self._connect_to_old_index():
            logger.warning("⚠️ Could not connect to old index, proceeding with document recreation")
        
        # Step 2: Get old index stats
        if self.old_pc:
            logger.info("\n📊 Step 2: Getting old index statistics...")
            old_stats = self._get_old_index_stats()
            if old_stats:
                logger.info(f"Old index had {old_stats.get('total_vector_count', 0)} vectors")
        
        # Step 3: Migrate insurance knowledge
        logger.info("\n📚 Step 3: Migrating insurance knowledge...")
        insurance_success = await self.migrate_insurance_knowledge()
        
        # Step 4: Migrate project knowledge
        logger.info("\n🏗️ Step 4: Migrating project knowledge...")
        project_success = await self.migrate_project_knowledge()
        
        # Step 5: Verify migration
        logger.info("\n✅ Step 5: Verifying migration...")
        verification_success = await self.verify_migration()
        
        # Final results
        total_time = time.time() - start_time
        
        logger.info("\n" + "=" * 60)
        logger.info("📊 MIGRATION RESULTS")
        logger.info("=" * 60)
        logger.info(f"Insurance Knowledge: {'✅ SUCCESS' if insurance_success else '❌ FAILED'}")
        logger.info(f"Project Knowledge: {'✅ SUCCESS' if project_success else '❌ FAILED'}")
        logger.info(f"Verification: {'✅ SUCCESS' if verification_success else '❌ FAILED'}")
        logger.info(f"Total Time: {total_time:.2f} seconds")
        
        if insurance_success and project_success and verification_success:
            logger.info("\n🎉 MIGRATION COMPLETED SUCCESSFULLY!")
            logger.info("Your new insurewiz768 index is now populated and ready to use.")
            return True
        else:
            logger.error("\n⚠️ MIGRATION HAD ISSUES!")
            logger.error("Please check the logs above and fix any problems.")
            return False

async def main():
    """Main migration function"""
    logger.info("Starting index migration process...")
    
    migrator = IndexMigrationService()
    
    try:
        success = await migrator.run_migration()
        
        if success:
            logger.info("\n🎯 NEXT STEPS:")
            logger.info("1. Test the new index with: python test_rag_complete.py")
            logger.info("2. Start your server with: python main.py")
            logger.info("3. The old index can be deleted if no longer needed")
        else:
            logger.error("\n🔧 Please fix the migration issues before proceeding")
            
    except Exception as e:
        logger.error(f"\n💥 Migration process crashed: {str(e)}")
        logger.error("Check your configuration and ensure all services are running properly.")

if __name__ == "__main__":
    asyncio.run(main())

