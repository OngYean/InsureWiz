"""
Tavily + Crawl4AI Web Scraping Pipeline Explanation
"""

# SCRAPING WORKFLOW:
# ==================

# 1. TAVILY API (URL Discovery):
# - Searches Google for insurer policy pages
# - Example: "Zurich Malaysia motor insurance comprehensive"
# - Returns relevant URLs from insurer websites
# - Filters for official company domains

# 2. CRAWL4AI (Content Extraction):
# - Takes URLs from Tavily
# - Extracts policy details, coverage, pricing
# - Converts web content to structured data
# - Handles dynamic content and JavaScript

# CURRENT STATUS:
# ===============

# Tavily: Configured but needs API key
tavily_searches = [
    "Zurich Malaysia comprehensive motor insurance",
    "Etiqa motor insurance coverage Malaysia", 
    "Allianz car insurance Malaysia pricing"
]

# Crawl4AI: Stub implementation (placeholder)
# - Framework ready
# - Needs full implementation
# - Will extract policy details from HTML

# REAL SCRAPING TARGETS:
# ======================

insurer_websites = {
    "Zurich": "https://www.zurich.com.my/en/products/general-insurance/motor",
    "Etiqa": "https://www.etiqa.com.my/v2/motor-insurance",
    "Allianz": "https://www.allianz.com.my/personal/motor-insurance",
    "Great Eastern": "https://www.greateasterngeneral.com/my/en/personal/motor-insurance",
    "Tokio Marine": "https://www.tokiomarine.com/my/personal/motor-insurance"
}

# DATA TO EXTRACT:
# ================

policy_fields_to_scrape = [
    "coverage_types",      # Comprehensive, Third Party
    "base_premiums",       # Starting prices
    "windscreen_cover",    # Coverage details
    "roadside_assistance", # Additional services  
    "exclusions",          # What's not covered
    "addon_options",       # Optional extras
    "claim_procedures",    # How to claim
    "contact_info"         # Support details
]

# SCRAPING FREQUENCY:
# ===================
# - Daily: Price updates
# - Weekly: Coverage changes  
# - Monthly: New products
# - As needed: Manual refresh
