"""
Simple Supabase client wrapper
"""

import os
from typing import Optional
from supabase import create_client, Client

_supabase_client: Optional[Client] = None

def get_supabase_client() -> Optional[Client]:
    """Get or create Supabase client"""
    global _supabase_client
    
    if _supabase_client is None:
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        
        if supabase_url and supabase_key:
            try:
                _supabase_client = create_client(supabase_url, supabase_key)
            except Exception as e:
                print(f"Failed to create Supabase client: {e}")
                return None
        else:
            print("Supabase credentials not found. Database operations will be disabled.")
            return None
    
    return _supabase_client

def is_database_available() -> bool:
    """Check if database is available"""
    return get_supabase_client() is not None
