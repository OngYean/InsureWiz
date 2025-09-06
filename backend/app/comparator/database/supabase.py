"""
Supabase client configuration and connection management
"""

import os
from typing import Optional
from supabase import create_client, Client
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class SupabaseClient:
    """Supabase client wrapper with connection management"""
    
    def __init__(self):
        self._client: Optional[Client] = None
        self._url = os.getenv("SUPABASE_URL")
        self._key = os.getenv("SUPABASE_KEY") or os.getenv("SUPABASE_ANON_KEY")  # Support both names
        
        if not self._url or not self._key:
            logger.warning("Supabase credentials not found. Database operations will be disabled.")
    
    @property
    def client(self) -> Optional[Client]:
        """Get or create Supabase client"""
        if not self._url or not self._key:
            return None
            
        if self._client is None:
            try:
                self._client = create_client(self._url, self._key)
                logger.info("Supabase client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Supabase client: {e}")
                return None
        
        return self._client
    
    def test_connection(self) -> bool:
        """Test the database connection"""
        if not self.client:
            return False
        
        try:
            # Try a simple query to test connection
            result = self.client.table("policies").select("id").limit(1).execute()
            return True
        except Exception as e:
            logger.error(f"Database connection test failed: {e}")
            return False
    
    def create_tables(self) -> bool:
        """Create necessary database tables if they don't exist"""
        if not self.client:
            logger.error("Cannot create tables: Supabase client not available")
            return False
        
        try:
            # SQL for creating the policies table
            policies_sql = """
            CREATE TABLE IF NOT EXISTS policies (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                insurer TEXT NOT NULL,
                product_name TEXT NOT NULL,
                is_takaful BOOLEAN DEFAULT FALSE,
                coverage_type TEXT NOT NULL,
                valuation_method TEXT,
                eligibility JSONB DEFAULT '{}',
                included_cover JSONB DEFAULT '{}',
                addons JSONB DEFAULT '{}',
                services JSONB DEFAULT '{}',
                pricing_notes JSONB DEFAULT '{}',
                exclusions TEXT[] DEFAULT '{}',
                source_urls TEXT[] DEFAULT '{}',
                last_checked TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
            """
            
            # SQL for creating indexes
            indexes_sql = [
                "CREATE INDEX IF NOT EXISTS idx_policies_insurer ON policies(insurer);",
                "CREATE INDEX IF NOT EXISTS idx_policies_coverage ON policies(coverage_type);",
                "CREATE INDEX IF NOT EXISTS idx_policies_takaful ON policies(is_takaful);",
                "CREATE INDEX IF NOT EXISTS idx_policies_updated ON policies(updated_at);"
            ]
            
            # SQL for comparison sessions table
            sessions_sql = """
            CREATE TABLE IF NOT EXISTS comparison_sessions (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                customer_data JSONB NOT NULL,
                comparison_results JSONB NOT NULL,
                pdf_path TEXT,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                expires_at TIMESTAMP WITH TIME ZONE DEFAULT (NOW() + INTERVAL '30 days')
            );
            """
            
            # Execute table creation
            self.client.rpc('exec_sql', {'sql': policies_sql}).execute()
            self.client.rpc('exec_sql', {'sql': sessions_sql}).execute()
            
            # Execute index creation
            for index_sql in indexes_sql:
                self.client.rpc('exec_sql', {'sql': index_sql}).execute()
            
            logger.info("Database tables created successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create database tables: {e}")
            return False

# Global instance
supabase_client = SupabaseClient()

def get_supabase_client() -> Optional[Client]:
    """Get the global Supabase client instance"""
    return supabase_client.client

def test_database_connection() -> bool:
    """Test database connection"""
    return supabase_client.test_connection()

def initialize_database() -> bool:
    """Initialize database with required tables"""
    return supabase_client.create_tables()
