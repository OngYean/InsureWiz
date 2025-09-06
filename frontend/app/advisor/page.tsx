import { Navigation } from "@/components/navigation"
import { InsuranceAdvisorChat } from "@/components/insurance-advisor-chat"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { MessageSquare, Brain, Globe, Clock, Shield, TrendingUp } from "lucide-react"

export default function AdvisorPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background to-muted/20">
      <Navigation />

      <main className="container mx-auto px-4 py-8 mobile-optimized">
        {/* Enhanced Header Section */}
        <div className="text-center mb-12 animate-fade-in-up">
          <div className="flex items-center justify-center mb-6">
            <div className="relative">
              <div className="w-16 h-16 bg-gradient-to-br from-primary to-secondary rounded-2xl flex items-center justify-center shadow-lg animate-float">
                <MessageSquare className="h-8 w-8 text-white" />
              </div>
              <div className="absolute -top-2 -right-2 w-6 h-6 bg-green-500 rounded-full border-4 border-background animate-pulse" />
            </div>
            <div className="ml-6 text-left">
              <h1 className="text-4xl font-bold gradient-text">
                AI Insurance Advisor
              </h1>
              <p className="text-xl text-muted-foreground mt-2">
                Your intelligent companion for insurance guidance
              </p>
            </div>
          </div>
          <p className="text-lg text-muted-foreground max-w-3xl mx-auto leading-relaxed">
            Get personalized insurance advice in plain English. Ask any question about coverage, policies, or claims. 
            Our AI-powered system provides instant, accurate guidance 24/7.
          </p>
        </div>

        <div className="grid grid-cols-1 xl:grid-cols-4 gap-8">
          {/* Enhanced Chat Interface - Now with proper height constraints */}
          <div className="xl:col-span-3">
            <div className="relative h-full">
              <div className="absolute -inset-1 bg-gradient-to-r from-primary/20 to-secondary/20 rounded-2xl blur-lg opacity-30" />
              <div className="relative h-full">
                <InsuranceAdvisorChat />
              </div>
            </div>
          </div>

          {/* Enhanced Info Panel */}
          <div className="space-y-6">
            {/* AI Features Card */}
            <Card className="border-border shadow-lg hover:shadow-xl transition-all duration-300 bg-gradient-to-br from-background to-muted/30 card-hover">
              <CardHeader className="pb-4">
                <CardTitle className="flex items-center text-lg text-foreground">
                  <div className="w-10 h-10 bg-gradient-to-br from-primary to-primary/80 rounded-xl flex items-center justify-center mr-3">
                    <Brain className="h-5 w-5 text-white" />
                  </div>
                  AI Features
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-start space-x-3 p-3 rounded-lg hover:bg-muted/50 transition-colors duration-200">
                  <MessageSquare className="h-5 w-5 text-green-500 mt-0.5 flex-shrink-0" />
                  <div>
                    <p className="font-semibold text-sm text-foreground">Natural Language</p>
                    <p className="text-xs text-muted-foreground">Explains complex insurance terms in simple English</p>
                  </div>
                </div>
                <div className="flex items-start space-x-3 p-3 rounded-lg hover:bg-muted/50 transition-colors duration-200">
                  <Globe className="h-5 w-5 text-blue-500 mt-0.5 flex-shrink-0" />
                  <div>
                    <p className="font-semibold text-sm text-foreground">Multilingual</p>
                    <p className="text-xs text-muted-foreground">
                      Supports questions and answers in multiple languages
                    </p>
                  </div>
                </div>
                <div className="flex items-start space-x-3 p-3 rounded-lg hover:bg-muted/50 transition-colors duration-200">
                  <Clock className="h-5 w-5 text-amber-500 mt-0.5 flex-shrink-0" />
                  <div>
                    <p className="font-semibold text-sm text-foreground">24/7 Available</p>
                    <p className="text-xs text-muted-foreground">Get instant answers anytime, anywhere</p>
                  </div>
                </div>
                <div className="flex items-start space-x-3 p-3 rounded-lg hover:bg-muted/50 transition-colors duration-200">
                  <Shield className="h-5 w-5 text-purple-500 mt-0.5 flex-shrink-0" />
                  <div>
                    <p className="font-semibold text-sm text-foreground">Secure & Private</p>
                    <p className="text-xs text-muted-foreground">Your conversations are encrypted and secure</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Popular Questions Card */}
            <Card className="border-border shadow-lg hover:shadow-xl transition-all duration-300 bg-gradient-to-br from-background to-muted/30 card-hover">
              <CardHeader className="pb-4">
                <CardTitle className="flex items-center text-lg text-foreground">
                  <div className="w-10 h-10 bg-gradient-to-br from-secondary to-secondary/80 rounded-xl flex items-center justify-center mr-3">
                    <TrendingUp className="h-5 w-5 text-blue-500" />
                  </div>
                  Popular Questions
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <button className="w-full text-left p-3 text-sm bg-muted/50 rounded-lg hover:bg-muted transition-all duration-200 hover:shadow-md border border-transparent hover:border-border/50 btn-hover">
                    "What's the difference between comprehensive and collision coverage?"
                  </button>
                  <button className="w-full text-left p-3 text-sm bg-muted/50 rounded-lg hover:bg-muted transition-all duration-200 hover:shadow-md border border-transparent hover:border-border/50 btn-hover">
                    "How much car insurance do I need?"
                  </button>
                  <button className="w-full text-left p-3 text-sm bg-muted/50 rounded-lg hover:bg-muted transition-all duration-200 hover:shadow-md border border-transparent hover:border-border/50 btn-hover">
                    "What factors affect my insurance premium?"
                  </button>
                  <button className="w-full text-left p-3 text-sm bg-muted/50 rounded-lg hover:bg-muted transition-all duration-200 hover:shadow-md border border-transparent hover:border-border/50 btn-hover">
                    "How do I file a claim?"
                  </button>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </main>
    </div>
  )
}
