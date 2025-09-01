-- Malaysian Motor Insurance Comparator Database Schema
-- Run these SQL commands in your Supabase SQL editor

-- 1. Policies table - stores extracted insurance policy data
CREATE TABLE IF NOT EXISTS policies (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    insurer VARCHAR(255) NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    coverage_type VARCHAR(100) NOT NULL,
    is_takaful BOOLEAN DEFAULT false,
    
    -- Policy details (JSONB for flexibility)
    coverage_details JSONB DEFAULT '{}',
    pricing JSONB DEFAULT '{}',
    eligibility_criteria JSONB DEFAULT '{}',
    additional_benefits JSONB DEFAULT '{}',
    exclusions JSONB DEFAULT '{}',
    
    -- Metadata
    source_urls TEXT[],
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT now(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    
    -- Indexes for better query performance
    CONSTRAINT unique_policy UNIQUE(insurer, product_name, coverage_type)
);

-- 2. Comparison sessions - stores customer comparisons
CREATE TABLE IF NOT EXISTS comparison_sessions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    session_id VARCHAR(255) UNIQUE NOT NULL,
    
    -- Customer input data
    customer_input JSONB NOT NULL,
    
    -- Comparison results
    comparison_result JSONB NOT NULL,
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- 3. Crawl sessions - tracks crawling activities
CREATE TABLE IF NOT EXISTS crawl_sessions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    session_id VARCHAR(255) UNIQUE NOT NULL,
    
    -- Crawl details
    insurers_crawled TEXT[],
    urls_discovered INTEGER DEFAULT 0,
    policies_extracted INTEGER DEFAULT 0,
    
    -- Status and timing
    status VARCHAR(50) DEFAULT 'pending',
    started_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    completed_at TIMESTAMP WITH TIME ZONE,
    
    -- Results
    crawl_results JSONB DEFAULT '{}'
);

-- 4. Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_policies_insurer ON policies(insurer);
CREATE INDEX IF NOT EXISTS idx_policies_coverage_type ON policies(coverage_type);
CREATE INDEX IF NOT EXISTS idx_policies_is_takaful ON policies(is_takaful);
CREATE INDEX IF NOT EXISTS idx_policies_created_at ON policies(created_at);

CREATE INDEX IF NOT EXISTS idx_comparison_sessions_created_at ON comparison_sessions(created_at);
CREATE INDEX IF NOT EXISTS idx_crawl_sessions_status ON crawl_sessions(status);

-- 5. Create updated_at trigger for comparison_sessions
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_comparison_sessions_updated_at 
    BEFORE UPDATE ON comparison_sessions 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- 6. Insert sample data for testing
INSERT INTO policies (insurer, product_name, coverage_type, is_takaful, coverage_details, pricing, eligibility_criteria) VALUES
(
    'Zurich Malaysia',
    'Z-Driver',
    'comprehensive',
    false,
    '{"windscreen_cover": true, "roadside_assistance": true, "flood_coverage": true, "riot_strike_coverage": true}',
    '{"base_premium": 2500, "excess": 500, "ncd_discount": 55}',
    '{"min_age": 21, "max_age": 75, "vehicle_age_max": 15, "license_years_min": 2}'
),
(
    'Etiqa',
    'Private Car Takaful',
    'comprehensive', 
    true,
    '{"windscreen_cover": true, "roadside_assistance": true, "flood_coverage": true, "legal_liability": true}',
    '{"base_premium": 2200, "excess": 400, "ncd_discount": 55}',
    '{"min_age": 18, "max_age": 70, "vehicle_age_max": 12, "license_years_min": 1}'
),
(
    'Allianz General',
    'Motor Comprehensive',
    'comprehensive',
    false,
    '{"windscreen_cover": true, "roadside_assistance": true, "theft_coverage": true, "accessories_cover": true}',
    '{"base_premium": 2800, "excess": 600, "ncd_discount": 55}',
    '{"min_age": 21, "max_age": 75, "vehicle_age_max": 20, "license_years_min": 2}'
);

-- 7. Verify the setup
SELECT 'Setup completed successfully!' as status;
SELECT COUNT(*) as sample_policies_count FROM policies;
