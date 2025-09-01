import { Navigation } from "@/components/navigation"
import { InsuranceAdvisorChat } from "@/components/insurance-advisor-chat"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { MessageSquare, Brain, Globe, Clock } from "lucide-react"

export default function AdvisorPage() {
  return (
    <div className="min-h-screen bg-background">
      <Navigation />

      <main className="container mx-auto px-4 py-8">
        {/* Header Section */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center mb-4">
            <MessageSquare className="h-10 w-10 text-primary mr-3" />
            <h1 className="text-3xl font-bold text-foreground">AI Insurance Advisor</h1>
          </div>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Get personalized insurance advice in plain English. Ask any question about coverage, policies, or claims.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Chat Interface */}
          <div className="lg:col-span-3">
            <InsuranceAdvisorChat />
          </div>

          {/* Info Panel */}
          <div className="space-y-6">
            <Card className="border-border">
              <CardHeader>
                <CardTitle className="flex items-center text-lg">
                  <Brain className="h-5 w-5 text-primary mr-2" />
                  AI Features
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-start space-x-3">
                  <MessageSquare className="h-5 w-5 text-green-500 mt-0.5 flex-shrink-0" />
                  <div>
                    <p className="font-medium text-sm">Natural Language</p>
                    <p className="text-xs text-muted-foreground">Explains complex insurance terms in simple English</p>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <Globe className="h-5 w-5 text-blue-500 mt-0.5 flex-shrink-0" />
                  <div>
                    <p className="font-medium text-sm">Multilingual</p>
                    <p className="text-xs text-muted-foreground">
                      Supports questions and answers in multiple languages
                    </p>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <Clock className="h-5 w-5 text-amber-500 mt-0.5 flex-shrink-0" />
                  <div>
                    <p className="font-medium text-sm">24/7 Available</p>
                    <p className="text-xs text-muted-foreground">Get instant answers anytime, anywhere</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="border-border">
              <CardHeader>
                <CardTitle className="text-lg">Popular Questions</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <button className="w-full text-left p-2 text-sm bg-muted/50 rounded-lg hover:bg-muted transition-colors">
                    "What's the difference between comprehensive and collision coverage?"
                  </button>
                  <button className="w-full text-left p-2 text-sm bg-muted/50 rounded-lg hover:bg-muted transition-colors">
                    "How much car insurance do I need?"
                  </button>
                  <button className="w-full text-left p-2 text-sm bg-muted/50 rounded-lg hover:bg-muted transition-colors">
                    "What factors affect my insurance premium?"
                  </button>
                  <button className="w-full text-left p-2 text-sm bg-muted/50 rounded-lg hover:bg-muted transition-colors">
                    "How do I file a claim?"
                  </button>
                </div>
              </CardContent>
            </Card>

            <Card className="border-border">
              <CardHeader>
                <CardTitle className="text-lg">Chat Stats</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-muted-foreground">Response Time</span>
                    <span className="font-bold text-green-600">&lt; 2s</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-muted-foreground">Satisfaction Rate</span>
                    <span className="font-bold text-primary">96%</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-muted-foreground">Languages</span>
                    <span className="font-bold text-secondary">12+</span>
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
