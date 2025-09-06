"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Checkbox } from "@/components/ui/checkbox"
import { Progress } from "@/components/ui/progress"
import { Skeleton } from "@/components/ui/skeleton"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { 
  Check, X, Star, Shield, DollarSign, Users, MapPin, Calendar, 
  RefreshCw, Download, TrendingUp, Brain, Zap, Clock,
  Car, CreditCard, User, Filter, BarChart3, FileText
} from "lucide-react"

import { 
  dynamicAPI, 
  CustomerInput, 
  PolicyData, 
  ComparisonResult,
  formatCurrency,
  calculateAnnualPremium,
  formatInsuranceCoverage
} from "@/lib/api/dynamic-insurance"

interface LoadingState {
  isLoading: boolean;
  currentStep: string;
  progress: number;
  completedInsurers: string[];
}

export function DynamicInsuranceComparison() {
  // State management
  const [customerInput, setCustomerInput] = useState<CustomerInput>({
    coverage_preference: "comprehensive",
    vehicle_type: "sedan",
    price_range_max: 3000,
    prefers_takaful: false
  });

  const [policies, setPolicies] = useState<PolicyData[]>([]);
  const [comparisonResults, setComparisonResults] = useState<ComparisonResult[]>([]);
  const [recommendation, setRecommendation] = useState<ComparisonResult | null>(null);
  const [marketAnalysis, setMarketAnalysis] = useState<any>(null);
  
  const [loadingState, setLoadingState] = useState<LoadingState>({
    isLoading: false,
    currentStep: "",
    progress: 0,
    completedInsurers: []
  });

  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState("filters");

  // Simulated insurers for progress tracking
  const insurers = ["Zurich Malaysia", "Etiqa", "Allianz General", "Great Eastern", "Tokio Marine"];

  // Simulate progress updates during scraping
  const simulateProgress = () => {
    let currentIndex = 0;
    const interval = setInterval(() => {
      if (currentIndex < insurers.length) {
        setLoadingState(prev => ({
          ...prev,
          currentStep: `Checking ${insurers[currentIndex]}...`,
          progress: ((currentIndex + 1) / insurers.length) * 100,
          completedInsurers: insurers.slice(0, currentIndex + 1)
        }));
        currentIndex++;
      } else {
        clearInterval(interval);
        setLoadingState(prev => ({
          ...prev,
          currentStep: "Analyzing results...",
          progress: 100
        }));
      }
    }, 3000); // 3 seconds per insurer

    return interval;
  };

  // Handle form input changes
  const updateCustomerInput = (field: string, value: any) => {
    setCustomerInput(prev => ({
      ...prev,
      [field]: value
    }));
  };

  // Main comparison function
  const handleGetLiveQuotes = async () => {
    setError(null);
    setLoadingState({
      isLoading: true,
      currentStep: "Preparing to scrape live data...",
      progress: 0,
      completedInsurers: []
    });
    setActiveTab("results");

    try {
      // Start progress simulation
      const progressInterval = simulateProgress();

      // Perform AI-powered comparison with live data
      const result = await dynamicAPI.compareWithAI(customerInput);
      
      // Clear progress simulation
      clearInterval(progressInterval);
      
      // Update state with results
      setComparisonResults(result.comparison_results || []);
      setRecommendation(result.recommendation || null);
      setMarketAnalysis(result.market_analysis || null);

      setLoadingState({
        isLoading: false,
        currentStep: "Complete!",
        progress: 100,
        completedInsurers: insurers
      });

    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
      setLoadingState({
        isLoading: false,
        currentStep: "",
        progress: 0,
        completedInsurers: []
      });
    }
  };

  // Generate PDF report
  const handleGenerateReport = async () => {
    if (!recommendation || comparisonResults.length === 0) return;

    try {
      const blob = await dynamicAPI.generatePDFReport({
        customer_input: customerInput,
        comparison_results: comparisonResults,
        recommendation: recommendation
      });

      // Download the PDF
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.style.display = 'none';
      a.href = url;
      a.download = `insurance-comparison-${Date.now()}.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      setError("Failed to generate PDF report");
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="text-center">
        <div className="flex items-center justify-center mb-4">
          <Brain className="h-8 w-8 text-primary mr-3" />
          <h2 className="text-2xl font-bold">AI-Powered Live Comparison</h2>
        </div>
        <p className="text-muted-foreground">
          Get real-time quotes from Malaysian insurers with AI analysis
        </p>
      </div>

      {/* Error Alert */}
      {error && (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* Main Content Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="filters" className="flex items-center gap-2">
            <Filter className="h-4 w-4" />
            Filters
          </TabsTrigger>
          <TabsTrigger value="results" className="flex items-center gap-2">
            <BarChart3 className="h-4 w-4" />
            Results
          </TabsTrigger>
          <TabsTrigger value="analysis" className="flex items-center gap-2">
            <TrendingUp className="h-4 w-4" />
            Analysis
          </TabsTrigger>
        </TabsList>

        {/* Filters Tab */}
        <TabsContent value="filters" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Car className="h-5 w-5" />
                Vehicle & Coverage Preferences
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Basic Filters */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="vehicle-type">Vehicle Type</Label>
                  <Select 
                    value={customerInput.vehicle_type || ""} 
                    onValueChange={(value) => updateCustomerInput("vehicle_type", value)}
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="Select vehicle type" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="sedan">Sedan</SelectItem>
                      <SelectItem value="suv">SUV</SelectItem>
                      <SelectItem value="hatchback">Hatchback</SelectItem>
                      <SelectItem value="mpv">MPV</SelectItem>
                      <SelectItem value="truck">Truck</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="coverage-type">Coverage Type</Label>
                  <Select 
                    value={customerInput.coverage_preference || ""} 
                    onValueChange={(value) => updateCustomerInput("coverage_preference", value)}
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="Select coverage" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="comprehensive">Comprehensive</SelectItem>
                      <SelectItem value="third_party">Third Party</SelectItem>
                      <SelectItem value="third_party_fire_theft">Third Party, Fire & Theft</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              {/* Budget & Preferences */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="max-budget">Maximum Annual Budget (RM)</Label>
                  <Input
                    id="max-budget"
                    type="number"
                    value={customerInput.price_range_max || ""}
                    onChange={(e) => updateCustomerInput("price_range_max", Number(e.target.value))}
                    placeholder="3000"
                  />
                </div>

                <div className="flex items-center space-x-2">
                  <Checkbox
                    id="takaful"
                    checked={customerInput.prefers_takaful || false}
                    onCheckedChange={(checked) => updateCustomerInput("prefers_takaful", checked)}
                  />
                  <Label htmlFor="takaful">Prefer Takaful products</Label>
                </div>
              </div>

              {/* Action Button */}
              <div className="flex justify-center pt-4">
                <Button 
                  onClick={handleGetLiveQuotes}
                  disabled={loadingState.isLoading}
                  size="lg"
                  className="flex items-center gap-2"
                >
                  {loadingState.isLoading ? (
                    <>
                      <RefreshCw className="h-4 w-4 animate-spin" />
                      Getting Live Quotes...
                    </>
                  ) : (
                    <>
                      <Zap className="h-4 w-4" />
                      Get Live Quotes Now
                    </>
                  )}
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Results Tab */}
        <TabsContent value="results" className="space-y-6">
          {/* Loading State */}
          {loadingState.isLoading && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Clock className="h-5 w-5" />
                  Fetching Live Data
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>{loadingState.currentStep}</span>
                    <span>{Math.round(loadingState.progress)}%</span>
                  </div>
                  <Progress value={loadingState.progress} className="w-full" />
                </div>
                
                {/* Completed Insurers */}
                <div className="flex flex-wrap gap-2">
                  {insurers.map((insurer) => (
                    <Badge 
                      key={insurer} 
                      variant={loadingState.completedInsurers.includes(insurer) ? "default" : "outline"}
                      className="flex items-center gap-1"
                    >
                      {loadingState.completedInsurers.includes(insurer) && <Check className="h-3 w-3" />}
                      {insurer}
                    </Badge>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Recommendation Card */}
          {recommendation && !loadingState.isLoading && (
            <Card className="border-green-200 bg-green-50">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-green-800">
                  <Star className="h-5 w-5" />
                  AI Recommendation
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <h3 className="font-semibold text-lg mb-2">
                      {recommendation.policy.product_name}
                    </h3>
                    <p className="text-sm text-muted-foreground mb-2">
                      by {recommendation.policy.insurer}
                    </p>
                    {recommendation.policy.source_urls && recommendation.policy.source_urls.length > 0 && (
                      <a 
                        href={recommendation.policy.source_urls[0]} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="text-sm text-blue-600 hover:text-blue-800 underline mb-3 inline-block"
                      >
                        View Official Policy →
                      </a>
                    )}
                    <div className="flex items-center gap-2 mb-3">
                      <Badge>{recommendation.policy.coverage_type}</Badge>
                      {recommendation.policy.is_takaful && <Badge variant="outline">Takaful</Badge>}
                      <div className="flex items-center gap-1">
                        <Star className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                        <span className="text-sm font-medium">
                          {recommendation.overall_score.toFixed(1)}/10
                        </span>
                      </div>
                    </div>
                    <p className="text-lg font-bold text-green-600">
                      {formatCurrency(calculateAnnualPremium(recommendation.policy.pricing))} /year
                    </p>
                  </div>
                  
                  <div className="space-y-3">
                    <div>
                      <h4 className="font-medium text-sm mb-1">Why this is recommended:</h4>
                      <ul className="text-sm space-y-1">
                        {recommendation.pros.slice(0, 3).map((pro, index) => (
                          <li key={index} className="flex items-start gap-2">
                            <Check className="h-3 w-3 text-green-600 mt-0.5 flex-shrink-0" />
                            {pro}
                          </li>
                        ))}
                      </ul>
                    </div>
                    
                    <Button 
                      onClick={handleGenerateReport}
                      variant="outline" 
                      size="sm"
                      className="flex items-center gap-2"
                    >
                      <Download className="h-4 w-4" />
                      Download Report
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}

          {/* Comparison Results */}
          {comparisonResults.length > 0 && !loadingState.isLoading && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {comparisonResults.map((result, index) => (
                <Card key={result.policy.id} className="relative">
                  {result === recommendation && (
                    <div className="absolute -top-2 -right-2">
                      <Badge className="bg-green-500">Recommended</Badge>
                    </div>
                  )}
                  
                  <CardHeader className="pb-3">
                    <div className="flex justify-between items-start">
                      <div>
                        <h3 className="font-semibold">{result.policy.product_name}</h3>
                        <p className="text-sm text-muted-foreground">{result.policy.insurer}</p>
                        {result.policy.source_urls && result.policy.source_urls.length > 0 && (
                          <a 
                            href={result.policy.source_urls[0]} 
                            target="_blank" 
                            rel="noopener noreferrer"
                            className="text-xs text-blue-600 hover:text-blue-800 underline mt-1 inline-block"
                          >
                            View Official Policy →
                          </a>
                        )}
                      </div>
                      <div className="flex items-center gap-1">
                        <Star className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                        <span className="text-sm font-medium">
                          {result.overall_score.toFixed(1)}
                        </span>
                      </div>
                    </div>
                  </CardHeader>
                  
                  <CardContent className="space-y-3">
                    {/* Price */}
                    <div className="text-center p-3 bg-muted rounded-lg">
                      <p className="text-2xl font-bold">
                        {formatCurrency(calculateAnnualPremium(result.policy.pricing))}
                      </p>
                      <p className="text-sm text-muted-foreground">per year</p>
                    </div>

                    {/* Coverage Features */}
                    <div>
                      <h4 className="font-medium text-sm mb-2">Coverage Features</h4>
                      <div className="space-y-1">
                        {formatInsuranceCoverage(result.policy.coverage_details).slice(0, 4).map((feature, idx) => (
                          <div key={idx} className="flex items-center gap-2 text-sm">
                            <Check className="h-3 w-3 text-green-600" />
                            {feature}
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Badges */}
                    <div className="flex flex-wrap gap-1">
                      <Badge variant="outline">{result.policy.coverage_type}</Badge>
                      {result.policy.is_takaful && <Badge variant="outline">Takaful</Badge>}
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}

          {/* Empty State */}
          {!loadingState.isLoading && comparisonResults.length === 0 && (
            <Card>
              <CardContent className="text-center py-8">
                <Shield className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                <h3 className="text-lg font-medium mb-2">No Results Yet</h3>
                <p className="text-muted-foreground mb-4">
                  Set your preferences and click "Get Live Quotes" to see real-time insurance options
                </p>
                <Button onClick={() => setActiveTab("filters")}>
                  Go to Filters
                </Button>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        {/* Analysis Tab */}
        <TabsContent value="analysis" className="space-y-6">
          {marketAnalysis && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Market Analysis */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <TrendingUp className="h-5 w-5" />
                    Market Analysis
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <p className="text-sm text-muted-foreground">Average Premium</p>
                    <p className="text-2xl font-bold">
                      {formatCurrency(marketAnalysis.average_premium)}
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Market Trends</p>
                    <p className="text-sm">{marketAnalysis.price_trends}</p>
                  </div>
                  {marketAnalysis.market_insights && (
                    <div>
                      <p className="text-sm text-muted-foreground mb-2">Key Insights</p>
                      <ul className="text-sm space-y-1">
                        {marketAnalysis.market_insights.slice(0, 3).map((insight: string, index: number) => (
                          <li key={index} className="flex items-start gap-2">
                            <Brain className="h-3 w-3 text-primary mt-0.5 flex-shrink-0" />
                            {insight}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </CardContent>
              </Card>

              {/* Category Scores */}
              {recommendation && (
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <BarChart3 className="h-5 w-5" />
                      Recommended Policy Scores
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    {Object.entries(recommendation.category_scores).map(([category, score]) => (
                      <div key={category}>
                        <div className="flex justify-between text-sm mb-1">
                          <span className="capitalize">{category.replace('_', ' ')}</span>
                          <span>{(score * 10).toFixed(1)}/10</span>
                        </div>
                        <Progress value={score * 100} className="h-2" />
                      </div>
                    ))}
                  </CardContent>
                </Card>
              )}
            </div>
          )}

          {!marketAnalysis && (
            <Card>
              <CardContent className="text-center py-8">
                <Brain className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                <h3 className="text-lg font-medium mb-2">No Analysis Data</h3>
                <p className="text-muted-foreground">
                  Run a comparison to see AI-powered market analysis
                </p>
              </CardContent>
            </Card>
          )}
        </TabsContent>
      </Tabs>
    </div>
  );
}
