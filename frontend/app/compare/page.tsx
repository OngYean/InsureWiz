import { Navigation } from "@/components/navigation"
import { InsurancePolicyComparison } from "@/components/insurance-policy-comparison"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { BarChart3, Filter, TrendingUp, Users } from "lucide-react"

export default function ComparePage() {
  return (
    <div className="min-h-screen bg-background">
      <Navigation />

      <main className="container mx-auto px-4 py-8">
        {/* Header Section */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center mb-4">
            <BarChart3 className="h-10 w-10 text-primary mr-3" />
            <h1 className="text-3xl font-bold text-foreground">Smart Comparison Tool</h1>
          </div>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Compare insurance policies side-by-side with intelligent filtering to find the perfect coverage for your
            needs.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Comparison Interface */}
          <div className="lg:col-span-3">
            <InsurancePolicyComparison />
          </div>

          {/* Info Panel */}
          <div className="space-y-6">
            <Card className="border-border">
              <CardHeader>
                <CardTitle className="flex items-center text-lg">
                  <Filter className="h-5 w-5 text-primary mr-2" />
                  Smart Filters
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-start space-x-3">
                  <Users className="h-5 w-5 text-blue-500 mt-0.5 flex-shrink-0" />
                  <div>
                    <p className="font-medium text-sm">Age-Based</p>
                    <p className="text-xs text-muted-foreground">Policies optimized for your age group</p>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <TrendingUp className="h-5 w-5 text-green-500 mt-0.5 flex-shrink-0" />
                  <div>
                    <p className="font-medium text-sm">Value-Based</p>
                    <p className="text-xs text-muted-foreground">Coverage matched to your vehicle's worth</p>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <BarChart3 className="h-5 w-5 text-amber-500 mt-0.5 flex-shrink-0" />
                  <div>
                    <p className="font-medium text-sm">Location-Based</p>
                    <p className="text-xs text-muted-foreground">Rates adjusted for your area's risk factors</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="border-border">
              <CardHeader>
                <CardTitle className="text-lg">Comparison Tips</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3 text-sm">
                  <div className="p-3 bg-blue-50 dark:bg-blue-950/20 rounded-lg border-l-4 border-l-blue-500">
                    <p className="font-medium text-blue-900 dark:text-blue-100">Coverage Limits</p>
                    <p className="text-blue-700 dark:text-blue-200 text-xs">
                      Higher limits mean better protection but cost more
                    </p>
                  </div>
                  <div className="p-3 bg-green-50 dark:bg-green-950/20 rounded-lg border-l-4 border-l-green-500">
                    <p className="font-medium text-green-900 dark:text-green-100">Deductibles</p>
                    <p className="text-green-700 dark:text-green-200 text-xs">
                      Higher deductibles lower premiums but increase out-of-pocket costs
                    </p>
                  </div>
                  <div className="p-3 bg-amber-50 dark:bg-amber-950/20 rounded-lg border-l-4 border-l-amber-500">
                    <p className="font-medium text-amber-900 dark:text-amber-100">Discounts</p>
                    <p className="text-amber-700 dark:text-amber-200 text-xs">
                      Look for multi-policy, safe driver, and loyalty discounts
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="border-border">
              <CardHeader>
                <CardTitle className="text-lg">Market Insights</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-muted-foreground">Avg. Premium</span>
                    <span className="font-bold text-primary">$1,483/year</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-muted-foreground">Best Value</span>
                    <span className="font-bold text-green-600">SafeGuard Plus</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-muted-foreground">Most Popular</span>
                    <span className="font-bold text-secondary">Premium Shield</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </main>
    </div>
  )
}
