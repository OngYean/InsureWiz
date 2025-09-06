"""
Fix database schema mismatch by properly transforming scraped data to match actual Supabase schema
"""

import asyncio
import os
from datetime import datetime
from app.comparator.services.real_time_scraper import RealTimePolicyScraper
from app.comparator.database.supabase import get_supabase_client


def transform_scraped_data_to_supabase_schema(scraped_data: dict) -> dict:
    """Transform scraped data to match the actual Supabase schema"""
    
    # Extract coverage details from scraped data
    coverage_details_raw = scraped_data.get("coverage_details", {})
    
    # Transform to match Supabase schema
    coverage_details = {
        "windscreen_cover": coverage_details_raw.get("windscreen_cover", False),
        "roadside_assistance": coverage_details_raw.get("roadside_assistance", False),
        "flood_coverage": coverage_details_raw.get("flood_coverage", False),
        "riot_strike_coverage": coverage_details_raw.get("riot_strike", False),
        "theft_coverage": True,  # Standard for comprehensive
        "legal_liability": coverage_details_raw.get("legal_liability", False),
        "accessories_cover": coverage_details_raw.get("accessories", False),
        "personal_accident": coverage_details_raw.get("personal_accident", False),
        "ehailing_coverage": coverage_details_raw.get("ehailing_coverage", False),
        "premium_waiver": coverage_details_raw.get("premium_waiver", False),
        "takaful_benefits": coverage_details_raw.get("takaful_benefits", False),
        "hibah_nominee": coverage_details_raw.get("hibah_nominee", False),
        "global_coverage": coverage_details_raw.get("global_coverage", False),
        "emergency_assistance": coverage_details_raw.get("emergency_assistance", False)
    }
    
    # Extract pricing information
    pricing_raw = scraped_data.get("pricing", {})
    pricing = {
        "base_premium": pricing_raw.get("base_premium", 2000),
        "service_tax": pricing_raw.get("service_tax", 120),
        "excess": 500,  # Standard excess
        "ncd_discount": 55,  # Max NCD
        "early_renewal_discount": pricing_raw.get("early_renewal_discount", 0),
        "online_discount": pricing_raw.get("online_discount", 5)
    }
    
    # Create eligibility criteria
    eligibility_criteria = {
        "min_age": 18,
        "max_age": 75,
        "vehicle_age_max": 15,
        "license_years_min": 1,
        "excluded_vehicle_types": [],
        "geographic_restrictions": []
    }
    
    # Additional benefits
    additional_benefits = {
        "roadside_assistance": coverage_details.get("roadside_assistance", False),
        "car_replacement": coverage_details_raw.get("car_replacement", False),
        "workshop_network": True,
        "online_claims": True,
        "mobile_app": True,
        "hour_hotline": True
    }
    
    # Exclusions (common ones)
    exclusions = [
        "Racing and speed trials",
        "War and nuclear risks", 
        "Pre-existing damage",
        "Driving under influence",
        "Unlicensed driving"
    ]
    
    # Build the transformed data matching Supabase schema
    transformed_data = {
        "insurer": scraped_data.get("insurer", "Unknown"),
        "product_name": scraped_data.get("product_name", "Standard Motor"),
        "coverage_type": scraped_data.get("coverage_type", "comprehensive"),
        "is_takaful": scraped_data.get("is_takaful", False),
        "coverage_details": coverage_details,
        "pricing": pricing,
        "eligibility_criteria": eligibility_criteria,
        "additional_benefits": additional_benefits,
        "exclusions": exclusions,
        "source_urls": [scraped_data.get("source_url", "")] if scraped_data.get("source_url") else []
    }
    
    return transformed_data


async def test_supabase_schema_insertion():
    """Test database insertion with data transformed to match actual Supabase schema"""
    
    print("🔧 TESTING SUPABASE SCHEMA INSERTION")
    print("=" * 50)
    
    # Get Supabase client
    client = get_supabase_client()
    if not client:
        print("❌ Failed to get database client")
        return
    
    # Initialize scraper
    scraper = RealTimePolicyScraper()
    
    try:
        # Get scraped data
        print("1. Scraping data...")
        policies = await scraper.scrape_all_insurers()
        print(f"   📦 Scraped {len(policies)} policies")
        
        if not policies:
            print("   ❌ No policies scraped")
            return
        
        # Transform and insert each policy
        print("\n2. Transforming and inserting policies...")
        successful_insertions = 0
        
        for i, policy_data in enumerate(policies[:3]):  # Test with first 3 policies
            try:
                # Transform the data to match Supabase schema
                transformed_data = transform_scraped_data_to_supabase_schema(policy_data)
                
                print(f"   🔄 Inserting policy {i+1}: {transformed_data['insurer']} - {transformed_data['product_name']}")
                
                # Insert into database
                result = client.table("policies").insert(transformed_data).execute()
                
                if result.data:
                    successful_insertions += 1
                    print(f"   ✅ Successfully inserted policy {i+1}")
                    print(f"      ID: {result.data[0].get('id', 'N/A')}")
                else:
                    print(f"   ❌ Failed to insert policy {i+1}: No data returned")
                    
            except Exception as e:
                print(f"   ❌ Error inserting policy {i+1}: {e}")
        
        print(f"\n📊 Results: {successful_insertions}/{len(policies[:3])} policies inserted successfully")
        
        # Verify insertion by counting records
        print("\n3. Verifying insertion...")
        try:
            count_result = client.table("policies").select("count", count="exact").execute()
            total_policies = count_result.count or 0
            print(f"   📊 Total policies in database: {total_policies}")
            
            # Get recent policies
            recent_result = client.table("policies").select("id, insurer, product_name, coverage_type, is_takaful, created_at").order("created_at", desc=True).limit(5).execute()
            if recent_result.data:
                print(f"   📋 Recent policies:")
                for policy in recent_result.data:
                    print(f"      - {policy.get('insurer')} - {policy.get('product_name')} ({'Takaful' if policy.get('is_takaful') else 'Conventional'})")
            
            print("\n4. Sample policy details:")
            if recent_result.data:
                sample_policy = recent_result.data[0]
                print(f"   📄 Sample: {sample_policy.get('insurer')} - {sample_policy.get('product_name')}")
                print(f"      Coverage: {sample_policy.get('coverage_type')}")
                print(f"      Takaful: {'Yes' if sample_policy.get('is_takaful') else 'No'}")
                print(f"      Created: {sample_policy.get('created_at')}")
        
        except Exception as e:
            print(f"   ❌ Error verifying insertion: {e}")
            
    except Exception as e:
        print(f"❌ Error in testing: {e}")


if __name__ == "__main__":
    asyncio.run(test_supabase_schema_insertion())
