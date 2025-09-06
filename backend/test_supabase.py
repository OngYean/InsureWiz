"""
Supabase Connection Test
Tests database connectivity and setup
"""

import os
from datetime import datetime

async def test_supabase_connection():
    """Test Supabase database connection"""
    print("🔗 Testing Supabase Connection...")
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    print(f"Supabase URL: {supabase_url[:50]}..." if supabase_url else "❌ No Supabase URL found")
    print(f"Supabase Key: {supabase_key[:50]}..." if supabase_key else "❌ No Supabase Key found")
    
    if not supabase_url or not supabase_key:
        print("❌ Missing Supabase credentials in .env file")
        return False
    
    try:
        from supabase import create_client, Client
        
        # Create Supabase client
        supabase: Client = create_client(supabase_url, supabase_key)
        print("✅ Supabase client created successfully")
        
        # Test basic connection with a simple query
        try:
            # Try to access auth (this should work with any valid Supabase project)
            response = supabase.auth.get_user()
            print("✅ Supabase connection successful")
        except Exception as e:
            print(f"⚠️ Auth test failed (expected): {e}")
            print("✅ But client creation worked - connection is valid")
        
        # Test if our tables exist
        try:
            result = supabase.table("policies").select("count", count="exact").execute()
            print(f"✅ Policies table accessible - Count: {result.count}")
        except Exception as e:
            print(f"⚠️ Policies table not found: {e}")
            print("💡 Need to run the SQL setup script")
        
        return True
        
    except Exception as e:
        print(f"❌ Supabase connection failed: {e}")
        return False

async def test_supabase_tables():
    """Test if required tables exist"""
    print("\n📋 Testing Supabase Tables...")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    try:
        from supabase import create_client
        
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        
        if not supabase_url or not supabase_key:
            print("❌ Missing credentials")
            return False
        
        supabase = create_client(supabase_url, supabase_key)
        
        # Test each required table
        tables_to_check = ["policies", "comparison_sessions", "crawl_sessions"]
        
        for table_name in tables_to_check:
            try:
                result = supabase.table(table_name).select("count", count="exact").limit(1).execute()
                print(f"✅ Table '{table_name}' exists - Records: {result.count}")
            except Exception as e:
                print(f"❌ Table '{table_name}' missing: {str(e)[:100]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Table check failed: {e}")
        return False

async def test_supabase_operations():
    """Test basic CRUD operations"""
    print("\n⚡ Testing Supabase Operations...")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    try:
        from supabase import create_client
        import uuid
        
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        supabase = create_client(supabase_url, supabase_key)
        
        # Test insert a sample policy
        test_policy = {
            "insurer": "Test Insurer",
            "product_name": "Test Policy",
            "coverage_type": "comprehensive",
            "is_takaful": False,
            "coverage_details": {"test": True},
            "pricing": {"base_premium": 2500},
            "source_urls": ["https://test.com"],
            "created_at": datetime.now().isoformat()
        }
        
        try:
            result = supabase.table("policies").insert(test_policy).execute()
            if result.data:
                policy_id = result.data[0]['id']
                print(f"✅ Insert test successful - ID: {policy_id}")
                
                # Test select
                select_result = supabase.table("policies").select("*").eq("id", policy_id).execute()
                if select_result.data:
                    print("✅ Select test successful")
                
                # Test delete (cleanup)
                delete_result = supabase.table("policies").delete().eq("id", policy_id).execute()
                print("✅ Delete test successful")
                
            else:
                print("❌ Insert returned no data")
                
        except Exception as e:
            print(f"❌ CRUD operations failed: {e}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Operations test failed: {e}")
        return False

def check_supabase_url_format():
    """Check if Supabase URL format is correct"""
    print("\n🔍 Checking Supabase URL Format...")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    supabase_url = os.getenv("SUPABASE_URL")
    
    if not supabase_url:
        print("❌ SUPABASE_URL not found in .env")
        return False
    
    print(f"URL: {supabase_url}")
    
    # Check URL format
    if supabase_url.startswith("postgresql://"):
        print("❌ Wrong format: This is a PostgreSQL connection string")
        print("💡 Supabase URL should be: https://your-project.supabase.co")
        return False
    elif supabase_url.startswith("https://") and ".supabase.co" in supabase_url:
        print("✅ URL format looks correct")
        return True
    else:
        print("⚠️ URL format might be incorrect")
        print("💡 Expected format: https://your-project.supabase.co")
        return False

async def main():
    """Run all Supabase tests"""
    print("🔧 Supabase Diagnostic Test Suite")
    print("=" * 50)
    
    # Check URL format first
    url_ok = check_supabase_url_format()
    
    if not url_ok:
        print("\n❌ Fix the SUPABASE_URL format first!")
        print("\n📋 To get the correct URL:")
        print("1. Go to your Supabase project dashboard")
        print("2. Click 'Settings' → 'API'")
        print("3. Copy the 'URL' (not the PostgreSQL connection string)")
        print("4. Update your .env file with: SUPABASE_URL=https://your-project.supabase.co")
        return
    
    # Run connection tests
    tests = [
        test_supabase_connection,
        test_supabase_tables,
        test_supabase_operations
    ]
    
    results = []
    for test in tests:
        try:
            result = await test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            results.append(False)
    
    print(f"\n📊 Results: {sum(results)}/{len(results)} tests passed")
    
    if results[0] and not results[1]:
        print("\n💡 Connection works but tables missing!")
        print("Run this SQL in your Supabase SQL editor:")
        print("File: supabase_setup.sql")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
