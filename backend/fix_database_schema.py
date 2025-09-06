"""
Fix database schema mismatch by properly transforming scraped data
"""

import asyncio
import os
from datetime import datetime
from app.comparator.services.real_time_scraper import RealTimeWebScraper
from app.comparator.database.supabase import get_supabase_client
from app.comparator.models.policy import PolicyRecord, CoverageType, IncludedCover, AddOns, Services, PricingNotes, Eligibility


def transform_scraped_data_to_policy_record(scraped_data: dict) -> dict:
    """Transform scraped data to match PolicyRecord database schema"""
    
    # Map coverage type
    coverage_type = scraped_data.get("coverage_type", "comprehensive").lower()
    if coverage_type == "comprehensive":
        coverage_type = CoverageType.COMPREHENSIVE
    elif coverage_type in ["third_party", "third party"]:
        coverage_type = CoverageType.THIRD_PARTY
    elif coverage_type in ["tpft", "third_party_fire_theft"]:
        coverage_type = CoverageType.TPFT
    else:
        coverage_type = CoverageType.COMPREHENSIVE
    
    # Extract coverage details
    coverage_details = scraped_data.get("coverage_details", {})
    
    # Create included cover object
    included_cover = IncludedCover(
        flood=coverage_details.get("flood_coverage", False),
        theft=True,  # Assume comprehensive includes theft
        windscreen=coverage_details.get("windscreen_cover", False),
        personal_accident=coverage_details.get("personal_accident", False),
        natural_disaster=coverage_details.get("flood_coverage", False),
        ehailing_coverage=coverage_details.get("ehailing_coverage", False)
    )
    
    # Create add-ons object
    addons = AddOns(
        roadside_assistance=coverage_details.get("roadside_assistance", False),
        car_replacement=coverage_details.get("car_replacement", False),
        enhanced_pa_cover=coverage_details.get("enhanced_pa", False),
        legal_liability_upgrade=coverage_details.get("legal_liability", False)
    )
    
    # Create services object
    services = Services(
        online_claims=coverage_details.get("online_claims", False),
        mobile_app=coverage_details.get("mobile_app", False),
        hour_hotline=coverage_details.get("24h_hotline", True),
        towing_service=coverage_details.get("roadside_assistance", False),
        workshop_network=True  # Most insurers have this
    )
    
    # Create pricing notes
    pricing_data = scraped_data.get("pricing", {})
    pricing_notes = PricingNotes(
        base_premium_range=[
            pricing_data.get("base_premium", 2000) * 0.8,
            pricing_data.get("base_premium", 2000) * 1.2
        ],
        service_tax_rate=6.0,  # Standard rate in Malaysia
        early_renewal_discount=pricing_data.get("early_renewal_discount", 0),
        online_discount=pricing_data.get("online_discount", 0),
        promotional_offers=pricing_data.get("promotions", [])
    )
    
    # Create eligibility object
    eligibility = Eligibility(
        min_vehicle_age=0,
        max_vehicle_age=15,  # Standard for most insurers
        min_driver_age=18,
        max_driver_age=65,
        min_license_years=1
    )
    
    # Build the transformed data
    transformed_data = {
        "insurer": scraped_data.get("insurer", "Unknown"),
        "product_name": scraped_data.get("product_name", "Standard Motor"),
        "is_takaful": scraped_data.get("is_takaful", False),
        "coverage_type": coverage_type.value,
        "valuation_method": "Market Value",  # Default for most policies
        "eligibility": eligibility.dict(),
        "included_cover": included_cover.dict(),
        "addons": addons.dict(),
        "services": services.dict(),
        "pricing_notes": pricing_notes.dict(),
        "exclusions": scraped_data.get("exclusions", []),
        "source_urls": [scraped_data.get("source_url", "")] if scraped_data.get("source_url") else [],
        "last_checked": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    return transformed_data


async def test_fixed_insertion():
    """Test database insertion with properly transformed data"""
    
    print("🔧 TESTING FIXED DATABASE INSERTION")
    print("=" * 50)
    
    # Get Supabase client
    client = get_supabase_client()
    if not client:
        print("❌ Failed to get database client")
        return
    
    # Initialize scraper
    real_time_scraper = RealTimeWebScraper()
    
    try:
        # Get scraped data
        print("1. Scraping data...")
        policies = await real_time_scraper.scrape_all_insurers()
        print(f"   📦 Scraped {len(policies)} policies")
        
        if not policies:
            print("   ❌ No policies scraped")
            return
        
        # Transform and insert each policy
        print("\n2. Transforming and inserting policies...")
        successful_insertions = 0
        
        for i, policy_data in enumerate(policies[:3]):  # Test with first 3 policies
            try:
                # Transform the data
                transformed_data = transform_scraped_data_to_policy_record(policy_data)
                
                print(f"   🔄 Inserting policy {i+1}: {transformed_data['insurer']} - {transformed_data['product_name']}")
                
                # Insert into database
                result = client.table("policies").insert(transformed_data).execute()
                
                if result.data:
                    successful_insertions += 1
                    print(f"   ✅ Successfully inserted policy {i+1}")
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
            recent_result = client.table("policies").select("*").order("updated_at", desc=True).limit(5).execute()
            if recent_result.data:
                print(f"   📋 Recent policies:")
                for policy in recent_result.data:
                    print(f"      - {policy.get('insurer')} - {policy.get('product_name')}")
        
        except Exception as e:
            print(f"   ❌ Error verifying insertion: {e}")
            
    except Exception as e:
        print(f"❌ Error in testing: {e}")


if __name__ == "__main__":
    asyncio.run(test_fixed_insertion())
