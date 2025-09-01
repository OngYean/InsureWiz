import { Navigation } from "@/components/navigation"
import { VehicleValidatorForm } from "@/components/vehicle-validator-form"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Car, CheckCircle, AlertCircle, Info } from "lucide-react"

export default function ValidatorPage() {
  return (
    <div className="min-h-screen bg-background">
      <Navigation />

      <main className="container mx-auto px-4 py-8">
        {/* Header Section */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center mb-4">
            <Car className="h-10 w-10 text-primary mr-3" />
            <h1 className="text-3xl font-bold text-foreground">Vehicle Data Validator</h1>
          </div>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Enter your vehicle information and get real-time validation with intelligent auto-correction suggestions.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Form */}
          <div className="lg:col-span-2">
            <VehicleValidatorForm />
          </div>

          {/* Info Panel */}
          <div className="space-y-6">
            <Card className="border-border">
              <CardHeader>
                <CardTitle className="flex items-center text-lg">
                  <Info className="h-5 w-5 text-primary mr-2" />
                  How It Works
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-start space-x-3">
                  <CheckCircle className="h-5 w-5 text-green-500 mt-0.5 flex-shrink-0" />
                  <div>
                    <p className="font-medium text-sm">Real-time Validation</p>
                    <p className="text-xs text-muted-foreground">
                      Instant feedback as you type with smart error detection
                    </p>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <AlertCircle className="h-5 w-5 text-amber-500 mt-0.5 flex-shrink-0" />
                  <div>
                    <p className="font-medium text-sm">Auto-correction</p>
                    <p className="text-xs text-muted-foreground">
                      Intelligent suggestions for typos and common mistakes
                    </p>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <Car className="h-5 w-5 text-primary mt-0.5 flex-shrink-0" />
                  <div>
                    <p className="font-medium text-sm">Confidence Scoring</p>
                    <p className="text-xs text-muted-foreground">See how confident we are in each validation result</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="border-border">
              <CardHeader>
                <CardTitle className="text-lg">Validation Stats</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-muted-foreground">Accuracy Rate</span>
                    <span className="font-bold text-green-600">99.2%</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-muted-foreground">Corrections Made</span>
                    <span className="font-bold text-primary">1.2M+</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-muted-foreground">Time Saved</span>
                    <span className="font-bold text-secondary">45 min/day</span>
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
