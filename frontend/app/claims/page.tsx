import { Navigation } from "@/components/navigation"
import { FraudClaimChecker } from "@/components/fraud-claim-checker"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { AlertTriangle, Shield, Eye, TrendingDown } from "lucide-react"

export default function ClaimsPage() {
  return (
    <div className="min-h-screen bg-background">
      <Navigation />

      <main className="container mx-auto px-4 py-8">
        {/* Header Section */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center mb-4">
            <AlertTriangle className="h-10 w-10 text-primary mr-3" />
            <h1 className="text-3xl font-bold text-foreground">Fraud & Claim Checker</h1>
          </div>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Advanced AI-powered analysis to detect suspicious patterns and prevent fraudulent insurance claims.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Main Checker Interface */}
          <div className="lg:col-span-3">
            <FraudClaimChecker />
          </div>

          {/* Info Panel */}
          <div className="space-y-6">
            <Card className="border-border">
              <CardHeader>
                <CardTitle className="flex items-center text-lg">
                  <Eye className="h-5 w-5 text-primary mr-2" />
                  Detection Methods
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-start space-x-3">
                  <Shield className="h-5 w-5 text-green-500 mt-0.5 flex-shrink-0" />
                  <div>
                    <p className="font-medium text-sm">Pattern Analysis</p>
                    <p className="text-xs text-muted-foreground">Identifies suspicious claim patterns and duplicates</p>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <AlertTriangle className="h-5 w-5 text-amber-500 mt-0.5 flex-shrink-0" />
                  <div>
                    <p className="font-medium text-sm">Risk Scoring</p>
                    <p className="text-xs text-muted-foreground">AI-powered risk assessment for each claim</p>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <TrendingDown className="h-5 w-5 text-red-500 mt-0.5 flex-shrink-0" />
                  <div>
                    <p className="font-medium text-sm">Anomaly Detection</p>
                    <p className="text-xs text-muted-foreground">Spots unusual claim amounts and circumstances</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="border-border">
              <CardHeader>
                <CardTitle className="text-lg">Fraud Prevention Stats</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-muted-foreground">Detection Rate</span>
                    <span className="font-bold text-green-600">94.7%</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-muted-foreground">False Positives</span>
                    <span className="font-bold text-amber-600">2.1%</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-muted-foreground">Money Saved</span>
                    <span className="font-bold text-primary">$2.4M</span>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="border-border">
              <CardHeader>
                <CardTitle className="text-lg">Common Red Flags</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3 text-sm">
                  <div className="p-3 bg-red-50 dark:bg-red-950/20 rounded-lg border-l-4 border-l-red-500">
                    <p className="font-medium text-red-900 dark:text-red-100">Duplicate Claims</p>
                    <p className="text-red-700 dark:text-red-200 text-xs">Same incident claimed multiple times</p>
                  </div>
                  <div className="p-3 bg-amber-50 dark:bg-amber-950/20 rounded-lg border-l-4 border-l-amber-500">
                    <p className="font-medium text-amber-900 dark:text-amber-100">Unusual Timing</p>
                    <p className="text-amber-700 dark:text-amber-200 text-xs">
                      Claims filed shortly after policy start
                    </p>
                  </div>
                  <div className="p-3 bg-orange-50 dark:bg-orange-950/20 rounded-lg border-l-4 border-l-orange-500">
                    <p className="font-medium text-orange-900 dark:text-orange-100">Excessive Amounts</p>
                    <p className="text-orange-700 dark:text-orange-200 text-xs">Claims significantly above average</p>
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
