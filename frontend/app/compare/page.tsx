import { Navigation } from "@/components/navigation"
import { DynamicInsuranceComparison } from "@/components/dynamic-insurance-comparison"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { BarChart3, Brain, Zap, TrendingUp, Shield, Clock } from "lucide-react"

export default function ComparePage() {
  return (
    <div className="min-h-screen bg-background">
      <Navigation />

      <main className="container mx-auto px-4 py-8">
        {/* Header Section */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center mb-4">
            <BarChart3 className="h-10 w-10 text-primary mr-3" />
            <h1 className="text-3xl font-bold text-foreground">Live Insurance Comparison</h1>
          </div>
          <p className="text-lg text-muted-foreground max-w-3xl mx-auto">
            Get real-time quotes from Malaysian insurers with AI-powered analysis and recommendations. 
            Compare policies instantly with live pricing and coverage data.
          </p>
        </div>

        {/* Features Banner */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <Card className="text-center border-primary/20 bg-primary/5">
            <CardContent className="pt-6">
              <Zap className="h-8 w-8 text-primary mx-auto mb-2" />
              <h3 className="font-semibold text-sm">Real-time Data</h3>
              <p className="text-xs text-muted-foreground">Live quotes from insurers</p>
            </CardContent>
          </Card>
          <Card className="text-center border-primary/20 bg-primary/5">
            <CardContent className="pt-6">
              <Brain className="h-8 w-8 text-primary mx-auto mb-2" />
              <h3 className="font-semibold text-sm">AI Analysis</h3>
              <p className="text-xs text-muted-foreground">Smart recommendations</p>
            </CardContent>
          </Card>
          <Card className="text-center border-primary/20 bg-primary/5">
            <CardContent className="pt-6">
              <TrendingUp className="h-8 w-8 text-primary mx-auto mb-2" />
              <h3 className="font-semibold text-sm">Market Insights</h3>
              <p className="text-xs text-muted-foreground">Pricing trends & analysis</p>
            </CardContent>
          </Card>
          <Card className="text-center border-primary/20 bg-primary/5">
            <CardContent className="pt-6">
              <Shield className="h-8 w-8 text-primary mx-auto mb-2" />
              <h3 className="font-semibold text-sm">Best Coverage</h3>
              <p className="text-xs text-muted-foreground">Tailored to your needs</p>
            </CardContent>
          </Card>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Main Comparison Interface */}
          <div className="lg:col-span-3">
            <DynamicInsuranceComparison />
          </div>

          {/* Info Panel */}
          <div className="space-y-6">
            <Card className="border-border">
              <CardHeader>
                <CardTitle className="flex items-center text-lg">
                  <Clock className="h-5 w-5 text-primary mr-2" />
                  How It Works
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-start space-x-3">
                  <div className="w-6 h-6 bg-primary text-primary-foreground rounded-full flex items-center justify-center text-xs font-bold">
                    1
                  </div>
                  <div>
                    <p className="font-medium text-sm">Set Your Preferences</p>
                    <p className="text-xs text-muted-foreground">Vehicle type, coverage, and budget</p>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <div className="w-6 h-6 bg-primary text-primary-foreground rounded-full flex items-center justify-center text-xs font-bold">
                    2
                  </div>
                  <div>
                    <p className="font-medium text-sm">Live Data Scraping</p>
                    <p className="text-xs text-muted-foreground">Real-time quotes from top insurers</p>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <div className="w-6 h-6 bg-primary text-primary-foreground rounded-full flex items-center justify-center text-xs font-bold">
                    3
                  </div>
                  <div>
                    <p className="font-medium text-sm">AI Analysis</p>
                    <p className="text-xs text-muted-foreground">Smart recommendations and insights</p>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <div className="w-6 h-6 bg-primary text-primary-foreground rounded-full flex items-center justify-center text-xs font-bold">
                    4
                  </div>
                  <div>
                    <p className="font-medium text-sm">Compare & Choose</p>
                    <p className="text-xs text-muted-foreground">Download detailed PDF report</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="border-border">
              <CardHeader>
                <CardTitle className="flex items-center text-lg">
                  <Shield className="h-5 w-5 text-primary mr-2" />
                  Covered Insurers
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                  <span className="text-sm">Zurich Malaysia</span>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                  <span className="text-sm">Etiqa</span>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                  <span className="text-sm">Allianz General</span>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                  <span className="text-sm">Great Eastern</span>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                  <span className="text-sm">Tokio Marine</span>
                </div>
              </CardContent>
            </Card>

            <Card className="border-border bg-muted/50">
              <CardHeader>
                <CardTitle className="flex items-center text-lg">
                  <Brain className="h-5 w-5 text-primary mr-2" />
                  AI Features
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="text-sm">
                  <p className="font-medium">✨ Smart Scoring</p>
                  <p className="text-xs text-muted-foreground">Multi-factor analysis for best match</p>
                </div>
                <div className="text-sm">
                  <p className="font-medium">📊 Market Analysis</p>
                  <p className="text-xs text-muted-foreground">Real-time pricing trends</p>
                </div>
                <div className="text-sm">
                  <p className="font-medium">🎯 Personalized</p>
                  <p className="text-xs text-muted-foreground">Tailored to your profile</p>
                </div>
                <div className="text-sm">
                  <p className="font-medium">📄 PDF Reports</p>
                  <p className="text-xs text-muted-foreground">Detailed comparison documents</p>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </main>
    </div>
  )
}
