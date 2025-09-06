// API service for dynamic insurance comparison
const API_BASE_URL = 'http://localhost:8000';

export interface CustomerInput {
  personal_info?: {
    age?: number;
    gender?: string;
    location?: string;
    annual_income?: number;
    driving_experience_years?: number;
  };
  vehicle_info?: {
    make?: string;
    model?: string;
    year?: number;
    engine_capacity?: number;
    vehicle_value?: number;
    vehicle_age?: number;
    ncd_percentage?: number;
    vehicle_type?: string;
  };
  preferences?: {
    coverage_preference: string;
    price_range_min?: number;
    price_range_max?: number;
    prefers_takaful?: boolean;
    preferred_insurers?: string[];
    important_features?: string[];
  };
  // Quick comparison fields
  vehicle_type?: string;
  coverage_preference?: string;
  price_range_max?: number;
  prefers_takaful?: boolean;
}

export interface PolicyData {
  id: string;
  insurer: string;
  product_name: string;
  coverage_type: string;
  is_takaful: boolean;
  coverage_details: {
    windscreen_cover: boolean;
    roadside_assistance: boolean;
    flood_coverage: boolean;
    riot_strike_coverage: boolean;
    theft_coverage: boolean;
    legal_liability: boolean;
    accessories_cover: boolean;
    personal_accident: boolean;
  };
  pricing: {
    base_premium: number;
    service_tax: number;
    excess: number;
    ncd_discount: number;
  };
  eligibility_criteria: {
    min_age: number;
    max_age: number;
    vehicle_age_max: number;
    license_years_min: number;
  };
  additional_benefits: {
    roadside_assistance: boolean;
    workshop_network: boolean;
    online_claims: boolean;
    mobile_app: boolean;
  };
  source_urls: string[];
  created_at?: string;
}

export interface ComparisonResult {
  policy: PolicyData;
  overall_score: number;
  category_scores: {
    coverage_score: number;
    price_score: number;
    service_score: number;
    eligibility_score: number;
  };
  pros: string[];
  cons: string[];
  ai_analysis: string;
  suitability_rating: string;
}

export interface ScrapingProgress {
  current_insurer: string;
  completed_insurers: string[];
  total_insurers: number;
  progress_percentage: number;
}

export class DynamicInsuranceAPI {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  // Health check
  async checkHealth(): Promise<boolean> {
    try {
      const response = await fetch(`${this.baseUrl}/dynamic/health`);
      return response.ok;
    } catch (error) {
      console.error('Health check failed:', error);
      return false;
    }
  }

  // Scrape all insurers with progress tracking
  async scrapeAllPolicies(onProgress?: (progress: ScrapingProgress) => void): Promise<{
    policies: PolicyData[];
    total_policies: number;
    stored_in_database: number;
  }> {
    const response = await fetch(`${this.baseUrl}/dynamic/scrape/all`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`Scraping failed: ${response.statusText}`);
    }

    const data = await response.json();
    return {
      policies: data.policies || [],
      total_policies: data.scraped_policies || 0,
      stored_in_database: data.stored_in_database || 0,
    };
  }

  // Get live policies (cached recent data)
  async getLivePolicies(filters?: {
    insurer?: string;
    coverage_type?: string;
    is_takaful?: boolean;
  }): Promise<{
    policies: PolicyData[];
    total_policies: number;
    data_freshness: string;
  }> {
    const params = new URLSearchParams();
    if (filters?.insurer) params.append('insurer', filters.insurer);
    if (filters?.coverage_type) params.append('coverage_type', filters.coverage_type);
    if (filters?.is_takaful !== undefined) params.append('is_takaful', filters.is_takaful.toString());

    const url = `${this.baseUrl}/dynamic/policies/live${params.toString() ? '?' + params.toString() : ''}`;
    const response = await fetch(url);

    if (!response.ok) {
      throw new Error(`Failed to get live policies: ${response.statusText}`);
    }

    return await response.json();
  }

  // AI-powered comparison with live data
  async compareWithAI(customerInput: CustomerInput): Promise<{
    comparison_results: ComparisonResult[];
    recommendation: ComparisonResult;
    market_analysis: {
      average_premium: number;
      price_trends: string;
      market_insights: string[];
    };
    data_freshness: string;
  }> {
    const response = await fetch(`${this.baseUrl}/dynamic/compare/live`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ customer_input: customerInput }),
    });

    if (!response.ok) {
      throw new Error(`Comparison failed: ${response.statusText}`);
    }

    return await response.json();
  }

  // Generate PDF report
  async generatePDFReport(comparisonData: {
    customer_input: CustomerInput;
    comparison_results: ComparisonResult[];
    recommendation: ComparisonResult;
  }): Promise<Blob> {
    const response = await fetch(`${this.baseUrl}/advanced/generate-report`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(comparisonData),
    });

    if (!response.ok) {
      throw new Error(`PDF generation failed: ${response.statusText}`);
    }

    return await response.blob();
  }

  // Advanced analysis with AI insights
  async getAdvancedAnalysis(customerInput: CustomerInput): Promise<{
    customer_profile: {
      risk_profile: string;
      suitable_coverage_types: string[];
      budget_analysis: string;
      recommendations: string[];
    };
    market_analysis: {
      average_premium: number;
      premium_range: [number, number];
      market_trends: string[];
      competitive_landscape: string[];
    };
    ai_insights: string[];
  }> {
    const response = await fetch(`${this.baseUrl}/advanced/analyze/comprehensive`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ customer_input: customerInput }),
    });

    if (!response.ok) {
      throw new Error(`Advanced analysis failed: ${response.statusText}`);
    }

    return await response.json();
  }
}

// Create singleton instance
export const dynamicAPI = new DynamicInsuranceAPI();

// Utility functions for formatting
export const formatCurrency = (amount: number): string => {
  return new Intl.NumberFormat('en-MY', {
    style: 'currency',
    currency: 'MYR',
    minimumFractionDigits: 0,
  }).format(amount);
};

export const calculateAnnualPremium = (pricing: PolicyData['pricing']): number => {
  return pricing.base_premium + pricing.service_tax;
};

export const formatInsuranceCoverage = (coverage: PolicyData['coverage_details']): string[] => {
  const features = [];
  if (coverage.windscreen_cover) features.push('Windscreen Cover');
  if (coverage.roadside_assistance) features.push('Roadside Assistance');
  if (coverage.flood_coverage) features.push('Flood Coverage');
  if (coverage.theft_coverage) features.push('Theft Protection');
  if (coverage.personal_accident) features.push('Personal Accident');
  if (coverage.legal_liability) features.push('Legal Liability');
  return features;
};
