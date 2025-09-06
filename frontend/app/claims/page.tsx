import { Navigation } from "@/components/navigation";
import { ClaimSuccessPredictorForm } from "@/components/claim-success-predictor-form";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Target,
  TrendingUp,
  Clock,
  CheckCircle,
  AlertTriangle,
  Brain,
  BarChart3,
} from "lucide-react";

export default function ClaimsPage() {
  return (
    <div className="min-h-screen bg-background">
      <Navigation />

      <main className="container mx-auto px-4 py-8">
        {/* Header Section */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center mb-4">
            <Target className="h-10 w-10 text-primary mr-3" />
            <h1 className="text-3xl font-bold text-foreground">
              Claim Success Predictor
            </h1>
          </div>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Estimate the likelihood of your motor insurance claim being
            successful. Get AI-powered insights before filing your claim.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Main Form */}
          <div className="lg:col-span-3">
            <ClaimSuccessPredictorForm />
          </div>

          {/* Sidebar - Prediction Info Cards */}
          <div className="lg:col-span-1 space-y-6">
            {/* Prediction Accuracy Info */}
            <Card className="top-8">
              <CardHeader>
                <CardTitle className="flex items-center text-lg">
                  <Brain className="h-5 w-5 text-primary mr-2" />
                  AI Prediction
                </CardTitle>
              </CardHeader>
              <CardContent className="text-sm space-y-4">
                <div className="p-3 bg-green-50 rounded-lg border-l-4 border-green-500">
                  <div className="flex items-start">
                    <TrendingUp className="h-5 w-5 text-green-500 mt-0.5 flex-shrink-0" />
                    <div className="ml-2">
                      <h4 className="font-semibold text-green-900">
                        High Accuracy
                      </h4>
                      <p className="text-green-700">
                        Get insights from AI trained on policy documents from
                        Malaysian insurance companies
                      </p>
                    </div>
                  </div>
                </div>
                <div className="p-3 bg-blue-50 rounded-lg border-l-4 border-blue-500">
                  <div className="flex items-start">
                    <BarChart3 className="h-5 w-5 text-blue-500 mt-0.5 flex-shrink-0" />
                    <div className="ml-2">
                      <h4 className="font-semibold text-blue-900">
                        Success Factors
                      </h4>
                      <p className="text-blue-700">
                        Incident type, documentation, timing
                      </p>
                    </div>
                  </div>
                </div>
                <div className="p-3 bg-purple-50 rounded-lg border-l-4 border-purple-500">
                  <div className="flex items-start">
                    <CheckCircle className="h-5 w-5 text-purple-500 mt-0.5 flex-shrink-0" />
                    <div className="ml-2">
                      <h4 className="font-semibold text-purple-900">
                        Instant Results
                      </h4>
                      <p className="text-purple-700">
                        Get prediction in seconds
                      </p>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Key Factors Card */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center text-lg">
                  <AlertTriangle className="h-5 w-5 text-amber-500 mr-2" />
                  Key Success Factors
                </CardTitle>
              </CardHeader>
              <CardContent className="text-sm space-y-3">
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                  <span>Police report filed within 24 hours</span>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                  <span>Clear photo evidence</span>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
                  <span>Valid insurance coverage</span>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-amber-500 rounded-full"></div>
                  <span>No policy violations</span>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-red-500 rounded-full"></div>
                  <span>Witness statements available</span>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </main>
    </div>
  );
}
